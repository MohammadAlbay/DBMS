using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace dbms.sql
{
    public enum SQLCommandType
    {
        SELECT = 1, SELECT_FROM = 2, SELECT_FROM_WHERE = 3, 
        INSERT = 4, UPDATE = 5, UPDATE_WHERE = 6, 
        DELETE = 7, DELETE_WHERE = 8, NONE = 9
    }

    public static class SQLCommandTypeAnalyzer
    {
        public static Regex SelectRegex = new Regex("^((?i)(select){1}\\s+)(.+)\\s*([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static Regex SelectFromRegex = new Regex("^((?i)(select){1}\\s+)(.+)(\\s+)(((?i)from){1})(\\s+)(\\w+)\\s*([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static Regex SelectFromWhereRegex = new Regex("^((?i)(select){1}\\s+)(.+)(\\s+)((?i)from){1}(\\s+)(\\w+)(\\s+)(((?i)where){1})(\\s+)(.+)\\s*([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static Regex InsertRegex = new Regex("^((?i)insert\\s+(?i)into)(\\s+)(\\w+)(\\s*)((\\()(.+)(\\)))((\\s*)(?i)values)(\\s*)((\\()(.+)(\\)))\\s*([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static Regex UpdateRegex = new Regex("^((?i)update\\s+)(\\w+)(\\s+)((?i)set)(\\s+)(.+)\\s*([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static Regex UpdateWhereRegex = new Regex("^((?i)update\\s+)(\\w+)(\\s+)((?i)set{1})(\\s+)(.+)(\\s+)(((?i)where){1})(\\s+)(.+)(\\s*)([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static Regex DeleteRegex = new Regex("^((?i)delete\\s+)((?i)from){1}(\\s+)(\\w+)(\\s*)([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static Regex DeleteWhereRegex = new Regex("^((?i)delete\\s+)((?i)from){1}(\\s+)(\\w+)(\\s+)(((?i)where){1})(\\s+)(.+)(\\s*)([;]$)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        public static SQLCommandType GetCommandType(string str)
        {

            if (SelectFromWhereRegex.IsMatch(str)) return SQLCommandType.SELECT_FROM_WHERE;
            else if (SelectFromRegex.IsMatch(str)) return SQLCommandType.SELECT_FROM;
            else if (SelectRegex.IsMatch(str)) return SQLCommandType.SELECT;
            else if (InsertRegex.IsMatch(str)) return SQLCommandType.INSERT;
            else if (UpdateWhereRegex.IsMatch(str)) return SQLCommandType.UPDATE_WHERE;
            else if (UpdateRegex.IsMatch(str)) return SQLCommandType.UPDATE;
            else if (DeleteWhereRegex.IsMatch(str)) return SQLCommandType.DELETE_WHERE;
            else if (DeleteRegex.IsMatch(str)) return SQLCommandType.DELETE;

            else return SQLCommandType.NONE;

        }


    }
}
