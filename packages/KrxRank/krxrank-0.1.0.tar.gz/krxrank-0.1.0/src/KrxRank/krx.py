import requests
import json
import pandas as pd

# 통계 - 기본통계 - 주식 - 종목시세 - 전종목시세
# input: 날짜 / output: [종목코드, 종목명, 시장구분, 시가총액]을 데이터프레임 형식으로 반환

def code_list(date):
    BASE_URL = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'data.krx.co.kr',
    'Origin': 'http://data.krx.co.kr',
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 126.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

    data = [
            ('bld', 'dbms/MDC/STAT/standard/MDCSTAT01501'),
            ('locale', 'ko_KR'),
            ('mktId', 'ALL'),
            ('trdDd', int(date)),
            ('share', '1'),
            ('csvxls_isNo', 'false')
        ]
    res = requests.post(BASE_URL, headers=headers, data=data)
    t = res.text
    want_list = json.loads(t)['OutBlock_1']
    Data = []
    for j in want_list:
        if str(j['MKT_NM']) == 'KONEX':
            pass
        else:
            code = j['ISU_SRT_CD']
            name = j['ISU_ABBRV']
            mk = j['MKT_NM']
            mk_cap = j['MKTCAP']
            Data.append([code, name, mk, mk_cap])
    df = pd.DataFrame(Data, columns=["종목코드", "종목명", "시장구분", "시가총액"])
    return df

print(code_list('20240723'))