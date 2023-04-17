using System.Text.RegularExpressions;

namespace dbms.sql
{
    public static class SQLScriptAnalyzer
    {
        public static SQLBlock Analyze(string sql) 
        { 
            SQLBlock block = new();
            int spacePosition = sql.IndexOf(' ');
            SQLCommandType commandType = SQLCommandTypeAnalyzer.GetCommandType(sql[0..spacePosition]);

            return block;
        }

        private static void Private_SelectAnalyze(ref SQLBlock block)
        {
            Regex SelectRegex = new Regex("select", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        }
    }
}