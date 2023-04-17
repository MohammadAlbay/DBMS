// See https://aka.ms/new-console-template for more information

using dbms.sql;
using System.Text.RegularExpressions;

// ([a-zA-Z]*)(\\d?)
//SQLBlock block = SQLScriptAnalyzer.Analyze("SELECT a,b,c FROM Table");

// select ... ; => ^((?i)(select){1}\s+)(.+)\s*([;]$)
// select ... from .. ; =>  ^((?i)(select){1}\s+)(.+)(\s+)(((?i)from){1})(\s+)(\w+)\s*([;]$)
// select ... from .. where .. ; => ^((?i)(select){1}\s+)(.+)(\s+)((?i)from){1}(\s+)(\w+)(\s+)(((?i)where){1})(\s+)(.+)\s*([;]$)
// update .. set ..=.. ; => ^((?i)update\s+)(\w+)(\s+)((?i)set)(\s+)(.+)\s*([;]$)
// update .. set ..=.. where .. ; => ^((?i)update\s+)(\w+)(\s+)((?i)set{1})(\s+)(.+)(\s+)(((?i)where){1})(\s+)(.+)(\s*)([;]$)
// insert into .. ( ..,..) values ( ..,..) ; => ^((?i)insert\s+(?i)into)(\s+)(\w+)(\s*)((\()(.+)(\)))((\s*)(?i)values)(\s*)((\()(.+)(\)))\s*([;]$)
// delete from .. ; => ^((?i)delete\s+)((?i)from){1}(\s+)(\w+)(\s*)([;]$)
// delete from .. where .. ; => ^((?i)delete\s+)((?i)from){1}(\s+)(\w+)(\s+)(((?i)where){1})(\s+)(.+)(\s*)([;]$)


Regex regex = new Regex("^((?i)update\\s+)(\\w+)(\\s+)((?i)set)(\\s+)(.+)\\s*([;]$)");
Console.WriteLine("matches {0}", regex.IsMatch("Update Table_1 Set Name = 'MD', Age = 15 WheRe ID = 5 || ID > 5;"));
Console.ReadKey();


//^(?i)(select){1}\s+(.+)\s((?i)from){1}\s+(\w+)\s+(((?i)where){1})\s+(.+)\s*[;]$
