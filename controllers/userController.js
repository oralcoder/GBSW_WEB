
const UserModel   = require('../models/userModel')
const { v4: uuidv4 } = require('uuid');
const hasher = require('pbkdf2-password')();

exports.renderSignupPage = async (req, res) => {
  res.render('signup');
}

exports.handleSignup = async (req, res) => {
  const { username, password, name, email } = req.body;

  hasher({ password: password }, async function (error, pass, salt, hash) {
    if (error) {
      console.error('비밀번호 해싱 오류:', error);
      return res.status(500).send('Internal Server Error');
    }

    const user = {
      id: uuidv4(),            // PostgreSQL UUID
      username: username,      // 사용자 ID
      password: hash,          // 해시된 비밀번호
      salt: salt,              // 솔트
      name: name,
      email: email
    };

    const result = await UserModel.AddUser(user);
    
    if (result.error) {
      console.log(result.error);
      res.redirect('/user/signup');
    } else {
      console.log('USER CREATED');
      res.redirect('/user/signin');
    }
  });
};

exports.renderSigninPage = (req, res) => {
  res.render('signin');
};

exports.handleSignin = async (req, res) => {
  const { username, password } = req.body;

  const user = await UserModel.FindUserByUsername(username);
  if (!user) {
    return res.redirect('/user/signin'); // 사용자 없음
  }

  hasher({ password, salt: user.salt }, (err, pass, salt, hash) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Internal Error');
    }

    if (hash === user.password) {
      req.session.username = user.username;
      req.session.isLoggedIn = true;
      return res.redirect('/'); // 로그인 성공 후 페이지
    } else {
      return res.redirect('/user/signin'); // 비밀번호 틀림
    }
  });
};

exports.handleSignout = (req, res) => {
  req.session.destroy(() => {
    res.clearCookie('connect.sid');
    res.redirect('/user/signin');
  });
};