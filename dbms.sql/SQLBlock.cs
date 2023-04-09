using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace dbms.sql
{
    public class SQLBlock
    {
        public SQLBlock() {}

        public SQLCommandType CommandType { get; set; };
        public bool HasConditionClause { get; internal set; }
        public bool HasFromClause { get; internal set; }
        public string DatabaseName { get; internal set; }
        public string TableName { get; internal set; }
        public string[] SelectedColumns { get; internal set; }
        public string[] SuppliedValues { get; internal set; }
    }
}
