const axios       = require('axios');
const cheerio     = require('cheerio');

exports.getDustData = async (req, res) => {
  // 1. 공공데이터포털 요청 파라미터 구성
  const url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty";
  const serviceKey = "Z8vfC6B5goJC0thf8CxwNLseqgzIswXrAUyLjf48PKn4nmg5X3AKcVuAqEsvzyj4z7b8E14ecffBqg67ITMfuA%3D%3D"; // 실제 인증키로 바꿔야 함
  const returnType = encodeURI("xml");
  const numOfRows = encodeURI("100");
  const pageNo = encodeURI("1");
  const sidoName = encodeURI("대구");
  const ver = encodeURI("1.0");

  const queryParams =
    '?' + encodeURI('serviceKey') + '=' + serviceKey +
    '&' + encodeURI('returnType') + '=' + returnType +
    '&' + encodeURI('numOfRows') + '=' + numOfRows +
    '&' + encodeURI('pageNo') + '=' + pageNo +
    '&' + encodeURI('sidoName') + '=' + sidoName +
    '&' + encodeURI('ver') + '=' + ver;

  console.log('queryParams: ', queryParams);

  try {
    const result = await axios.get(url + queryParams);
    const xml = result.data;

    // 2. cheerio로 XML 파싱
    const $ = cheerio.load(xml);
    const itemList = $('item');

    const context = [];

    itemList.each(function (index, item) {
      const stationName = $(item).find('stationName').text();
      const pm10Value = $(item).find('pm10Value').text();
      const pm25Value = $(item).find('pm25Value').text();

      context.push({
        stationName,
        pm10Value,
        pm25Value
      });
    });

    // 3. EJS 템플릿에 데이터 전달
    res.render('dust', { context });

  } catch (error) {
    console.error('미세먼지 데이터 요청 실패:', error.message);
    res.status(500).send('미세먼지 데이터를 가져오는 중 오류가 발생했습니다.');
  }
};