using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Windows;
using System.Windows.Forms;
using AIGS.Common;
using AIGS.Helper;

namespace Tidal
{
    public class TidalSession
    {
        static string URL_LOGIN = "https://login.tidal.com/";
        static string REDIRECT_URI_ANDROID = "https://tidal.com/android/login/auth";
        static string REDIRECT_URI_IOS = "tidal://login/auth";
        CookieContainer cookie = new CookieContainer();

        public string UserID;
        public string AccessToken;
        public string CountryCode;


        static string GetUrl(string sUrlPre, Dictionary<string, string> pData)
        {
            StringBuilder str = new StringBuilder();
            foreach (string key in pData.Keys)
                str.AppendFormat("&{0}={1}", key, System.Web.HttpUtility.UrlEncode(pData[key]));

            string sTmp = str.ToString().Substring(1);
            return sUrlPre + '?' + sTmp;
        }

        static string GetValueFromCookies(CookieContainer cc, string key)
        {
            Hashtable table = (Hashtable)cc.GetType().InvokeMember("m_domainTable", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.GetField | System.Reflection.BindingFlags.Instance, null, cc, new object[] { });
            StringBuilder sb = new StringBuilder();
            foreach (object pathList in table.Values)
            {
                SortedList lstCookieCol = (SortedList)pathList.GetType().InvokeMember("m_list", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.GetField | System.Reflection.BindingFlags.Instance, null, pathList, new object[] { });
                foreach (CookieCollection colCookies in lstCookieCol.Values)
                    foreach (Cookie c in colCookies)
                    {
                        if (c.Name == key)
                            return c.Value;
                    }
            }
            return null;
        }

        bool Valid(string sToken, ref string sUserID, ref string sCountryCode)
        {
            string sErrmsg;
            string sRet = (string)HttpHelper.GetOrPost("https://api.tidal.com/v1/sessions", out sErrmsg, Cookie: cookie, Timeout: 30 * 1000, UserAgent: null, Header: GetHeader(sToken));
            if (sErrmsg.IsNotBlank())
                return false;

            sUserID = JsonHelper.GetValue(sRet, "userId");
            sCountryCode = JsonHelper.GetValue(sRet, "countryCode");
            return true;
        }

        public string GetHeader(string sToken = null)
        {
            if (sToken.IsBlank())
                sToken = AccessToken;
            if (sToken.IsBlank())
                return "";
            return "authorization:Bearer " + sToken;
        }


        public string Login(string sUsername, string sPassword, string ClientID = "ck3zaWMi8Ka_XdI0", string sToken = null)
        {
            string ClientUniqueKey = Guid.NewGuid().ToString().Replace("-", "");
            string CodeVerifier = (Guid.NewGuid().ToString() + Guid.NewGuid().ToString()).Replace("-", "").Substring(0, 43);

            byte[] bytes = Encoding.UTF8.GetBytes(CodeVerifier);
            byte[] hash = SHA256Managed.Create().ComputeHash(bytes);
            string CodeChallenge = System.Convert.ToBase64String(hash);
            CodeChallenge = CodeChallenge.Substring(0, CodeChallenge.Length - 1);

            //Check old token
            string sTmpUserID = null;
            string sTmpCountryCode = null;
            if (sToken.IsNotBlank() && Valid(sToken, ref sTmpUserID, ref sTmpCountryCode))
            {
                UserID = sTmpUserID;
                CountryCode = sTmpCountryCode;
                AccessToken = sToken;
                return "";
            }

            //Login
            string sRet;
            string postJ;
            string sErrmsg;
            string sOauthCode;

            Dictionary<string, string> pParams = new Dictionary<string, string>() {
                {"response_type", "code" },
                {"lang", "en_US" },
                {"appMode", "android"},
                {"code_challenge_method", "S256"},
                {"redirect_uri", REDIRECT_URI_ANDROID},
                {"client_id", ClientID},
                {"client_unique_key", ClientUniqueKey},
                {"code_challenge", CodeChallenge}};

            sRet = (string)HttpHelper.GetOrPost(GetUrl(URL_LOGIN + "authorize", pParams), out sErrmsg, Cookie: cookie, Timeout: 30 * 1000, UserAgent:null);
            string csrf = GetValueFromCookies(cookie, "token");

            //email, verify email is valid
            postJ = "{" + string.Format("\"_csrf\":\"{0}\", \"email\":\"{1}\", \"recaptchaResponse\":\"\" ", csrf, sUsername) +"}";
            sRet = (string)HttpHelper.GetOrPost(GetUrl(URL_LOGIN + "email", pParams), out sErrmsg, Cookie: cookie,IsErrResponse: true, UserAgent: null, Timeout: 30 * 1000, PostJson: postJ, ContentType: "application/json;charset=UTF-8");
            if (sErrmsg.IsNotBlank())
                return "Unknown in https://login.tidal.com/email";
            if (JsonHelper.GetValue(sRet, "isValidEmail") != "True")
                return "Invalid email";
            if (JsonHelper.GetValue(sRet, "newUser") == "True")
                return "User does not exist";

            //login with user credentials
            postJ = "{" + string.Format("\"_csrf\":\"{0}\", \"email\":\"{1}\", \"password\":\"{2}\" ", csrf, sUsername, sPassword) + "}";
            sRet = (string)HttpHelper.GetOrPost(GetUrl(URL_LOGIN + "email/user/existing", pParams), out sErrmsg, Cookie: cookie, IsErrResponse: true, UserAgent: null, Timeout: 30 * 1000, PostJson: postJ, ContentType: "application/json;charset=UTF-8");
            if (JsonHelper.GetValue(sRet, "error").IsNotBlank())
            {
                sErrmsg = JsonHelper.GetValue(sRet, "error", "message");
                if(sErrmsg.IsBlank())
                    sErrmsg = "Unknown in https://login.tidal.com/email/user/existing";
            }
            if (sErrmsg.IsNotBlank())
                return "Unknown in https://login.tidal.com/email/user/existing";

            //retrieve access code
            sRet = (string)HttpHelper.GetOrPost(URL_LOGIN + "success?lang=en", out sErrmsg, Cookie: cookie, Timeout: 30 * 1000, UserAgent: null, AllowAutoRedirect:false);
            if (sErrmsg.IsNotBlank())
                return "Unknown in https://login.tidal.com/success?lang=en";
            sOauthCode = StringHelper.GetSubString(sRet, "code=", "&");

            //exchange access code for oauth token
            sRet = (string)HttpHelper.GetOrPost("https://auth.tidal.com/v1/oauth2/token", out sErrmsg, Cookie: cookie, Timeout: 30 * 1000, UserAgent: null, PostData: new Dictionary<string, string>() { 
                {"code", sOauthCode },
                {"client_id", ClientID },
                {"grant_type", "authorization_code" },
                {"redirect_uri", REDIRECT_URI_ANDROID },
                {"scope", "r_usr w_usr w_sub" },
                {"code_verifier", CodeVerifier },
                {"client_unique_key", ClientUniqueKey },
            });
            if (sErrmsg.IsNotBlank())
                return "Unknown in https://auth.tidal.com/v1/oauth2/token";
            AccessToken = JsonHelper.GetValue(sRet, "access_token");


            if(!Valid(AccessToken, ref UserID, ref CountryCode))
            {
                AccessToken = null;
                return "Unknown in https://api.tidal.com/v1/sessions";
            }
            
            return null;
        }
    }
}
