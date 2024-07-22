import textwrap
import time
import traceback

import sqlalchemy.orm.session

import cfg
import db
import db.digistore
import db.work_queue
import digistore.api as api
import utils
import log
import ses
from digistore.api import check_request
from user import get_user


PRODUCTS_CACHE = {} # XXX replace with a more sophisticated cache + re-enable


def store_processed_purchase(purchase_obj, user_id, session):
    purchase_id = purchase_obj['id']
    now = int(time.time()) # POSIX time (int only)

    tx = db.digistore.DigistoreTransaction(
        transaction_id=purchase_id,
        process_timestamp=now,
        user_id=user_id,
    )
    session.add(tx)


def is_transaction_unprocessed(transaction_obj, session):
    transaction_id = transaction_obj['id']
    processed = bool(
        session.query(db.digistore.DigistoreTransaction).filter_by(
            transaction_id=transaction_id,
        ).first()
    )
    return not processed

def retrieve_and_process_recent_purchases(session: sqlalchemy.orm.session.Session=None):
    if session is None:
        session = db.sa_session()

    # process last two days for now
    response = check_request('listTransactions', {'from': '-2d'})
    transactions = response['data']['transaction_list']
    log.log_str(f'retrieved {len(transactions)} transaction(s)')

    # filter out transactions that were already processed
    unprocessed_purchases = [
        tx for tx in transactions
        if is_transaction_unprocessed(transaction_obj=tx, session=session)
    ]
    log.log_str(f'thereof found {len(unprocessed_purchases)} transactions')

    for purchase in unprocessed_purchases:
        try:
            log.log_str(f'processing purchase with id {purchase["id"]}')
            process_purchase(purchase, session)
        except:
            purchase_id = purchase['id']
            traceback.print_exc()
            log.log_str(str(traceback.format_exc()))
            log.error_mail(
                'unexpected error whilst processing transaction ' + str(purchase_id) +
                ' error details: ' + str(traceback.format_exc())
            )


def is_first_payment(purchase_object):
    if not purchase_object.get('billing_type') == 'subscription':
        return True # non-subscriptions (i.e. single payments) are always "firsts"

    purchase_id = purchase_object.get('purchase_id')
    response = check_request('getPurchase', {'purchase_id': purchase_id})
    transactions = response['data'].get('transaction_list', [])

    if len(transactions) < 2:
        return True
    else:
        return False


MIETVORSORGE_FEATURE_ID = 6 # XXX HACK HACK HACK

def process_purchase(purchase_object, session):
    product_id = purchase_object['main_product_id']
    product_obj = retrieve_product_details(product_id)
    purchase_id = purchase_object['id']

    # collect data we require to grant access to filmportal
    product_tags = product_obj.tag
    try:
        product_grants = product_obj.product_grants()
    except RuntimeError as rte:
        log.log_str(rte.message)
        message = 'failed to process purchase (product_id: {p}): {e}'.format(
            p=product_id,
            e=str(rte)
        )
        return log.error_mail(message)

    log.log_str(f'purchase_id: {purchase_id} defines tags: {product_tags}')

    customer = purchase_object['buyer']

    allowed_feature_ids = product_grants.granted_feature_ids
    log.log_str(f'purchase_id: {purchase_id} grants feature(s): {allowed_feature_ids}')
    # XXX hack hack hack
    onboard_filmportal = True
    if MIETVORSORGE_FEATURE_ID in allowed_feature_ids:
        onboard_mivo = True
        if len(allowed_feature_ids) == 1:
            onboard_filmportal = False
    else:
        onboard_mivo = False

    log.digistore_mail(
        textwrap.dedent(
        f'''
    This is to inform you that digistore-tx with id {purchase_id} for digistore product identified by:
    {product_id}
    has been processed to grant the user identified by {customer['email']}:

    videos: {product_grants.granted_film_ids}
    video_sequences: {product_grants.granted_video_sequence_ids}
    features: {product_grants.granted_feature_ids}
    quota: {product_grants.granted_feature_quotas}

    for a duration (if applicable) of {product_grants.valid_time_in_days} day(s)

    Additional details on the tx, that may be helpful for debugging or tracing purposes:

    billing_type: {purchase_object.get('billing_type')}
    transaction_type: {purchase_object.get('transaction_type')}
    transaction_pay_method: {purchase_object.get('transaction_pay_method')}
        ''',
        ),
        tx_id=purchase_id,
    )

    utils.grant_user_access(
        user_email=customer['email'],
        user_first_name=customer['first_name'],
        user_last_name=customer['last_name'],
        product_grants=product_grants,
        purchase_id=purchase_id,
        session=session,
    )
    session.commit()

    if onboard_mivo:
        utils.init_mietvorsorge_feature(
            email=customer['email'],
            first_name=customer['first_name'],
            last_name=customer['last_name'],
            feature_id=MIETVORSORGE_FEATURE_ID,
        )

    # transactional semantics for each order processing
    try:
        if is_first_payment(purchase_object):
            first_payment = True
            try:
                if onboard_filmportal:
                    utils.send_onboarding_mail(
                        first_name=customer['first_name'],
                        last_name=customer['last_name'],
                        email_address=customer['email'],
                    )
                if onboard_mivo:
                    utils.send_onboarding_mail_mietvorsorge(
                        first_name=customer['first_name'],
                        last_name=customer['last_name'],
                        email_address=customer['email'],
                    )

            except Exception:
                # do not fail / rollback upon failed onboarding mailing
                # --> log / send error mails instead. Onboarding can be done
                # manually in worst-case
                # XXX: this is a workaround because rolling back will keep a dirty
                # DB. better approach would be to properly cleanup db.
                email = customer.get('email')
                print(f'Error: failed to send onboarding mail to {email}')
                log.log_str(traceback.format_exc())
                log.error_mail(traceback.format_exc())
                log.log_str(f'failed to send onboarding email: {email}')
        else:
            first_payment = False

        new_user = get_user(email=customer['email'], session=session)
        user_id = new_user.id

        global_cfg = cfg.cfgdc()
        aws_cfg = global_cfg.aws

        if first_payment and aws_cfg and aws_cfg.ses:
            ses_client = ses.ses_client(aws_cfg=aws_cfg)
            ses.send_validation_email(
                ses_client=ses_client,
                email_address=new_user.email_address,
                email_template_name=aws_cfg.ses.registration_template_mail_name,
            )

            # schedule patching user's email-address after validation
            queue_email_patching_after_validation = db.work_queue.WorkQueueEntry(
                type=db.work_queue.TypeNames.SES_VERIFICATION,
                data={
                    'user_id': user_id,
                    'email_address': new_user.email_address,
                },
                min_retry_wait_time_seconds=60*10, # 10 minutes
            )
            session.add(queue_email_patching_after_validation)

        store_processed_purchase(purchase_object, user_id, session)

        session.commit()
    except:
        session.rollback()


def retrieve_product_details(product_id):
    if product_id in PRODUCTS_CACHE and False: # XXX disable caching for now
        return PRODUCTS_CACHE[product_id]

    # if cache is missed, we have to fetch _all_ products
    # as the API does not offer us filtering
    products = api.list_products()
    for product in products:
        id = product.id
        PRODUCTS_CACHE[id] = product

    return PRODUCTS_CACHE[product_id]
