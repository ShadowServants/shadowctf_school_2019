using System;
using System.Security.Cryptography;
using System.Text;

namespace ReverseApi
{
    public class Crypto
    {
        public static string GetHash(string s)
        {
            var md5 = MD5.Create();
            var hash = md5.ComputeHash(Encoding.UTF8.GetBytes(s));
            return Convert.ToBase64String(hash);
        }

        public static string XorStrings(string a, string b)
        {
            StringBuilder sb = new StringBuilder();
            if (a.Length != b.Length)
            {
                return "";
            }
            for (int i = 0; i < a.Length; i++)
            {
                var x = a[i] ^ b[i];
                sb.Append(x.ToString("X"));
            }

            return sb.ToString();
        }
        public static string Reverse( string s )
        {
            char[] charArray = s.ToCharArray();
            Array.Reverse( charArray );
            return new string( charArray );
        }
    }
}