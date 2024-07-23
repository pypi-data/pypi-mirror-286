from __future__ import annotations
import re
from typing import Generator
from rst_fast_parse.core import gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_, gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__
from rst_fast_parse.elements import BasicElement, ElementListBase
from rst_fast_parse.regexes.block import gAAAAABmnuojneQp8ioMt4Crvi2R3rai5pmJHhAMYtpyCB89KPUG4KcNA8A2N5nvgkl6zY6Bdl3srM_UTRsplNXNzH5M2JgxyA__
from rst_fast_parse.source import PositiveInt, gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__

def gAAAAABmnuojzQozNQXGnjhsSixWPIRlwBCg6OTCx6UECXIug85i9vXxN33tZq9Eds_tzzZtKW4OQ6FxMVJ_7DZbhG_QBTZ7tg5GtpkdH7g5gKd9TNiopIs_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, _context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_:
    if not (_current_line := source.current_line):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__
    if not (_ := re.match(gAAAAABmnuojneQp8ioMt4Crvi2R3rai5pmJHhAMYtpyCB89KPUG4KcNA8A2N5nvgkl6zY6Bdl3srM_UTRsplNXNzH5M2JgxyA__, _current_line.content)):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__
    items = list(gAAAAABmnuojDP7aYyfGdH2Cdn2EnY7Hv_OuV0AQmqT_h9kx6goTuLdf_OJEE4m7Dhe5cB2207T1WQBKvWj96Pw3AqNxJGA51sUfk9uSccvHd_7WqNb4kuM_(source))
    if items:
        first = items[0][0].current_line
        last = items[-1][1].last_line or items[-1][0].last_line
        assert first and last
        parent.append(BasicElement('field_list', (first.line, last.line)))
    return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__

def gAAAAABmnuojDP7aYyfGdH2Cdn2EnY7Hv_OuV0AQmqT_h9kx6goTuLdf_OJEE4m7Dhe5cB2207T1WQBKvWj96Pw3AqNxJGA51sUfk9uSccvHd_7WqNb4kuM_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, /) -> Generator[tuple[gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__], None, None]:
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            continue
        if (match := re.match(gAAAAABmnuojneQp8ioMt4Crvi2R3rai5pmJHhAMYtpyCB89KPUG4KcNA8A2N5nvgkl6zY6Bdl3srM_UTRsplNXNzH5M2JgxyA__, current_line.content)):
            name_slice = current_line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(PositiveInt(match.start(1)), PositiveInt(match.end(1))).gAAAAABmnuojqnxMGqI1dncCL6wnTaj1f9xRGw6qA0lRVm1FssaY41gX73xvy3eP_TViCOLI5yoI4c4_slZbaTATlvkhgptDIQ__()
            body_slice = source.gAAAAABmnuojE0sYzkyFiqkGch85WYnsBvxpSsWEDOAyu6fnrOTGmq5i8vxuUbKHNHIbgq92u_ta1r_465lW6tMmp2ZI4EIybmsXLwScIEmasFmGdTUvFq4_(first_indent=match.end(0), advance=True)
            yield (name_slice, body_slice)
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
        else:
            source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
            break