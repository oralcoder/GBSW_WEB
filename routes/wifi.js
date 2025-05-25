const express     = require('express');
const router      = express.Router();
const wifiController = require('../controllers/wifiController');

router.get('/init', function(req, res) {
    wifiController.initWifiData(req, res);
});

router.get('/', (req, res) => {
  wifiController.getWifiData(req, res, null); // 전체 목록
});

router.get('/:provider', function(req, res) {
    const provider = req.params.provider || null;
    wifiController.getWifiData(req, res, provider);
});

module.exports = router;