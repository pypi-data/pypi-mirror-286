from __future__ import annotations
from enum import Enum
from typing import Protocol, Sequence
from rst_fast_parse.elements import BasicElementList, ElementListBase
from rst_fast_parse.source import gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__

class gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__:

    def __init__(self, block_parsers: Sequence[gAAAAABmnuojQyqeDaQy__YnlWrGwcnNDnxX3WFc5sEYCq3YNFNSjWOb8708Q0QAEfAGoVBcddyFfkxZXO22_vMDLeo3VErrAQ__], *, allow_titles: bool=True) -> None:
        self._allow_titles = allow_titles
        self._block_parsers = block_parsers

    @property
    def allow_titles(self) -> bool:
        return self._allow_titles

    def gAAAAABmnuojYfYikgFo6Xpz3o5GeAuyIG5Bm4jQ_phZM7QycxRg1nU_VOerZBtHPWnuPvpkVCeF744MIjsw1gNze_GW_gXZXQ__(self, source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__) -> ElementListBase:
        end_of_file = False
        parent = BasicElementList()
        while not end_of_file:
            for parser in self._block_parsers:
                result = parser(source, parent, self)
                if result == gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__:
                    break
                elif result == gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__:
                    continue
                elif result == gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__:
                    end_of_file = True
                    break
                else:
                    raise RuntimeError(f'Unknown parser result: {result!r}')
            else:
                if (line := source.current_line):
                    raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            if source.is_empty:
                break
        return parent

    def gAAAAABmnuojh_uCUc9p_qboeu___0Y623_dmRGgGK9eIxcOroGcZfNyHo4yfXtf2BSj_Bb88t_1GzyVT6sC5Zx8f41eMyg0qA__(self, source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, /) -> None:
        old_allow_titles = self._allow_titles
        try:
            self._allow_titles = False
            end_of_file = False
            while not end_of_file:
                for parser in self._block_parsers:
                    result = parser(source, parent, self)
                    if result == gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__:
                        break
                    elif result == gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__:
                        continue
                    elif result == gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__:
                        end_of_file = True
                        break
                    else:
                        raise RuntimeError(f'Unknown parser result: {result!r}')
                else:
                    if (line := source.current_line):
                        raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
                source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
                if source.is_empty:
                    break
        finally:
            self._allow_titles = old_allow_titles

class gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_(Enum):
    gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__ = 0
    'The parser successfully matched the input.'
    gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__ = 1
    'The parser did not match the input.'
    gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__ = 2
    'The parser reached the end of the file.'

class gAAAAABmnuojQyqeDaQy__YnlWrGwcnNDnxX3WFc5sEYCq3YNFNSjWOb8708Q0QAEfAGoVBcddyFfkxZXO22_vMDLeo3VErrAQ__(Protocol):

    def __call__(self, source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_:
        pass