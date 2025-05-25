const db = require('./database');

module.exports = {
  InsertInitWifiData: async function(wifiArray) {
    try {
      const query = `
        INSERT INTO wifis (inst_loc, inst_loc_detail, provider, inst_addr, latitude, longitude)
        VALUES ($1, $2, $3, $4, $5, $6)
      `;
      for (let wifi of wifiArray) {
        await db.query(query, wifi); //wifi는 배열로각 요소는 
      }                              //[inst_loc, inst_loc_detail, provider, inst_addr, latitude, longitude]
      return { rowCount: wifiArray.length };
    } catch (error) {
      console.error('WiFi 데이터 삽입 오류:', error);
      throw error;
    }
  },
  GetWiFiData: async function(provider = null) {
    try {
      let query = 'SELECT * FROM wifis';
      const values = [];

      if (provider) {
        query += ' WHERE provider = $1';
        values.push(provider);
      } 
      query += ' ORDER BY id';

      const result = await db.query(query, values);
      return result.rows;
  } catch (error) {
    console.error('WiFi 데이터 조회 오류:', error);
    throw error;
  }
  },
};