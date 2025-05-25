const express     = require('express');
const router      = express.Router();
const dustController = require('../controllers/dustController');

router.get('/', function(req, res) {
    dustController.getDustData(req, res);
});

module.exports = router;