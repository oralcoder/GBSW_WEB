const db = require('./database');

module.exports = {
  AddUser: async function(user) {
    try {
      const query = `
        INSERT INTO users (id, username, password, salt, name, email)
        VALUES ($1, $2, $3, $4, $5, $6)
      `;
      const values = [
        user.id,
        user.username,
        user.password,
        user.salt,
        user.name,
        user.email
      ];

      const result = await db.query(query, values);
      return { result, error: null };
    } catch (error) {
      return { result: null, error };
    }
  },
  FindUserByUsername: async function(username) {
    try {
      const query = `SELECT * FROM users WHERE username = $1`;
      const result = await db.query(query, [username]);
      return result.rows[0];
    } catch (error) {
      return null;
    }
  },
};