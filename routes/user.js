const express     = require('express');
const router      = express.Router();
const userController = require('../controllers/userController');

router.get('/signup', async function(req, res) {
	userController.renderSignupPage(req, res);
});
router.post('/signup', async function(req, res) {
	userController.handleSignup(req, res);
});
router.get('/signin', async (req, res) => {
  userController.renderSigninPage(req, res);
});
router.post('/signin', async (req, res) => {
  userController.handleSignin(req, res);
});
router.get('/signout', async (req, res) => {
  userController.handleSignout(req, res);
});
module.exports = router;