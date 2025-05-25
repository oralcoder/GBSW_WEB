const { Pool } = require('pg');
require('dotenv').config();

const db = new Pool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  max: 10, // 연결 풀 최대 개수
});

module.exports = db;
