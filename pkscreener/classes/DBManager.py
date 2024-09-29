"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""
try:
    import libsql_experimental as libsql
except:
    pass
import pyotp

from PKDevTools.classes.log import default_logger

class PKUser:
    userid=0
    username=""
    name=""
    email=""
    mobile=0
    passkey=""
    totptoken=""
    licensekey=""

    def userFromDBRecord(row):
        user = PKUser()
        user.userid= row[0]
        user.username= row[1]
        user.name= row[2]
        user.email= row[3]
        user.mobile= row[4]
        user.passkey= row[5]
        user.totptoken= row[6]
        user.licensekey= row[7]
        return user

class DBManager:
    def __init__(self):
        from dotenv import dotenv_values
        try:
            local_secrets = dotenv_values(".env.dev")
            self.url = local_secrets["TDU"]
            self.token = local_secrets["TAT"]
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            self.url = None
            self.token = None
        self.conn = None
    
    def shouldSkipLoading(self):
        skipLoading = False
        try:
            import libsql_experimental as libsql
        except:
            skipLoading = True
            pass
        return skipLoading
    
    def connection(self):
        try:
            if self.conn is None:
                self.conn = libsql.connect("pkscreener.db", sync_url=self.url, auth_token=self.token)
                self.conn.sync()
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            pass
        return self.conn

    def validateOTP(self,userIDOrName,otp):
        try:
            otpValue = 0
            dbUsers = self.getUserByIDorUsername(userIDOrName)
            if len(dbUsers) > 0:
                token = dbUsers[0].totptoken
                if token is not None:
                    otpValue = int(pyotp.TOTP(token).now())
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            pass
        return otpValue == int(otp) and otpValue > 0

    def getOTP(self,userID,username,name,retry=False):
        try:
            otpValue = 0
            dbUsers = self.getUserByID(int(userID))
            if not retry:
                if len(dbUsers) > 0:
                    token = dbUsers[0].totptoken
                    if token is not None:
                        otpValue = pyotp.TOTP(token).now()
                    else:
                        # Update user
                        user = PKUser.userFromDBRecord([userID,username.lower(),name,dbUsers[0].email,dbUsers[0].mobile,dbUsers[0].passkey,pyotp.random_base32(),dbUsers[0].licensekey])
                        self.updateUser(user)
                        return self.getOTP(userID,username,name,retry=True)
                else:
                    # Insert user
                    user = PKUser.userFromDBRecord([userID,username.lower(),name,None,None,None,pyotp.random_base32(),None])
                    self.insertUser(user)
                    return self.getOTP(userID,username,name,retry=True)
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            pass
        return otpValue

    def getUserByID(self,userID):
        try:
            users = []
            cursor = self.connection().cursor()
            records = cursor.execute(f"SELECT * FROM users WHERE userid=?",(self.sanitisedIntValue(userID),)).fetchall()
            for row in records:
                users.append(PKUser.userFromDBRecord(row))
            cursor.close()
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            pass
        return users

    def getUserByIDorUsername(self,userIDOrusername):
        try:
            users = []
            cursor = self.connection().cursor()
            try:
                userID = int(userIDOrusername)
            except:
                userID = 0
                pass
            records = cursor.execute(f"SELECT * FROM users WHERE userid=? or username=?",(self.sanitisedIntValue(userID),self.sanitisedStrValue(userIDOrusername.lower()),)).fetchall()
            for row in records:
                users.append(PKUser.userFromDBRecord(row))
            cursor.close()
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            pass
        return users
    
    def insertUser(self,user:PKUser):
        try:
            self.connection().execute(f"INSERT INTO users(userid,username,name,email,mobile,passkey,totptoken,licensekey) VALUES ({self.sanitisedIntValue(user.userid)},{self.sanitisedStrValue(user.username.lower())},{self.sanitisedStrValue(user.name)},{self.sanitisedStrValue(user.email)},{self.sanitisedIntValue(user.mobile)},{self.sanitisedStrValue(user.passkey)},{self.sanitisedStrValue(user.totptoken)},{self.sanitisedStrValue(user.licensekey)});")
            self.connection().commit()
            self.connection().sync()
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            pass
    
    def sanitisedStrValue(self,param):
        return "''" if param is None else f"'{param}'"

    def sanitisedIntValue(self,param):
        return param if param is not None else 0

    def updateUser(self,user:PKUser):
        try:
            self.connection().execute(f"UPDATE users SET username=?,name=?,email=?,mobile=?,passkey=?,totptoken=?,licensekey=? WHERE userid=?",(self.sanitisedStrValue(user.username.lower()),self.sanitisedStrValue(user.name),self.sanitisedStrValue(user.email),self.sanitisedIntValue(user.mobile),self.sanitisedStrValue(user.passkey),self.sanitisedStrValue(user.totptoken),self.sanitisedStrValue(user.licensekey),self.sanitisedIntValue(user.userid)))
            self.connection().commit()
            self.connection().sync()
        except Exception as e:
            default_logger().debug(e, exc_info=True)
            pass