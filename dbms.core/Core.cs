using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace dbms.core
{
    
    internal class Core
    {

        public static Database OpenDatabase(string filePath, DatabaseType databaseType) 
        {
            return new Database(); 
        }
    }
}
