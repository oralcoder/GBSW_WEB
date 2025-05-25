const xlsx        = require('xlsx');
const WifiModel   = require('../models/wifiModel')

exports.initWifiData = async (req, res) => {
  try {
    const wifiData = await WifiModel.GetWiFiData();
    if (wifiData.length > 0) {
      return res.status(400).send('WiFi 데이터가 이미 존재합니다. 초기화할 수 없습니다.');
    }
    const excelFile = xlsx.readFile('./12_04_07_E_무료와이파이정보.xlsx');
    const sheet = excelFile.Sheets[excelFile.SheetNames[0]];
    const wifiList = xlsx.utils.sheet_to_json(sheet);
     
    const wifiArray = [];

    for(const wifi of wifiList) {
        const temp = [
          wifi['설치장소명'], 
          wifi['설치장소상세'],
          wifi['서비스제공사명'],
          wifi['소재지도로명주소'],
          wifi['WGS84위도'],
          wifi['WGS84경도']
        ];
        wifiArray.push(temp);
    }
    const result = await WifiModel.InsertInitWifiData(wifiArray);
    res.send(`WiFi 데이터 ${result.rowCount}건이 초기화되었습니다.`);

  } catch (error) {
    console.error('WiFi 데이터 초기화 오류:', error);
    res.status(500).send('Internal Server Error');
  }  
};
exports.getWifiData = async (req, res, provider) => {
  try {
    const wifiData = await WifiModel.GetWiFiData(provider);
    res.render('wifi', { wifiData, provider });
  } catch (error) {
    console.error('WiFi 조회 오류:', error);
    res.status(500).send('Internal Server Error');
  }  
};