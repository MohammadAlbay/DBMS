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
        public SQLBlock(SQLBlock outer)
        {
            OuterBlock = outer;
        }
        public SQLBlock(SQLBlock outer, SQLBlock inner) 
        {
            OuterBlock = outer;
            InnerBlock = inner;
        }

        public SQLCommandType CommandType { get; set; }
        public bool HasConditionClause { get; internal set; }
        public bool HasFromClause { get; internal set; }
        public string DatabaseName { get; internal set; }
        public string TableName { get; internal set; }
        public string[] SelectedColumns { get; internal set; }
        public string[] SuppliedValues { get; internal set; }
        public SQLBlock InnerBlock { get; internal set; } = null;
        public SQLBlock OuterBlock { get; internal set; } = null;
        public short Depth { 
            get {
                short value = 0;
                SQLBlock block = OuterBlock;
                while(block != null)
                {
                    block = block.OuterBlock;
                    value++;
                }
                return value; 
            } 
            set { 
                Depth = value; 
            }  
        }


    }
}
