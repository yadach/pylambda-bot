import json
import logging

import yaml

from pylambda_bot import message_services
from pylambda_bot import nlp_engines


def lambda_handler(event, context):
    logging.info(f"Received event: {json.dumps(event)}")
    conf_file = "config.yaml"
    with open(conf_file, "r") as f:
        conf = yaml.safe_load(f)
    msg_svc = getattr(message_services, conf["message-service"]["name"])(
        **conf["message-service"].get("params", {})
    )
    nlp_model = getattr(nlp_engines, conf["nlp-engine"]["name"])(
        params=conf["nlp-engine"]["params"],
        initial_prompts=conf["nlp-engine"].get("initial_prompts", None),
    )
    try:
        input_text = msg_svc.parse_event(event)
    except message_services.MsgSrvRetryError:
        res_data = msg_svc.gen_res("Ignored due to timeout retry request.")
        return res_data
    conv_hist = msg_svc.get_conv_hist()
    tmp_msg_info = msg_svc.post("しばらくお待ち下さい...")
    res_text = nlp_model.get_reply(input_text, conv_hist)
    _ = msg_svc.delete(tmp_msg_info)
    _ = msg_svc.post(res_text)
    res_data = msg_svc.gen_res(input_text)
    return res_data
