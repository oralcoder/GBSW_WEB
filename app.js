const express   = require('express');
const app       = express();
const session   = require('express-session');

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use(session({
  secret: 'your-secret-key',         // 세션 암호화 키 (임의로 설정)
  resave: false,                     // 세션 값이 변경된 경우만 저장
  saveUninitialized: false,          // 로그인 등 세션 데이터 생성 시 저장
  cookie: {
    maxAge: 1000 * 60 * 60           // 세션 유지 시간 (1시간)
  }
}));

//라우트 객체 생성
const mainRouter    = require('./routes/index');
const dustRouter    = require('./routes/dust');
const userRouter    = require('./routes/user');
const wifiRouter    = require('./routes/wifi');

//라우트 설정
app.use('/', mainRouter);
app.use('/dust', dustRouter);
app.use('/user', userRouter);
app.use('/wifi', wifiRouter);

const PORT = 8080;
app.listen(PORT, function() {
    console.log('Listening on port: ', PORT);
});