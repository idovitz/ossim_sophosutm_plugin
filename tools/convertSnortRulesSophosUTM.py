#!/usr/bin/python3

import re, sys

def parseRule(rule):
	snortRule = {}
	rule = rule[rule.find("("):].replace("\"","")
	#print(rule)
	for ruleParam in re.findall("\w+:.*?;", rule):
		ruleParam = ruleParam.replace(";", "").split(":")
		#print(ruleParam)
		snortRule[ruleParam[0].strip()] = ruleParam[1].strip()
	
	return snortRule

f = open(sys.argv[1], 'r')
lines = f.readlines()

sql = """DELETE FROM plugin WHERE id = "4444";
DELETE FROM plugin_sid where plugin_id = "4444";

INSERT INTO plugin (id, type, name, description, product_type, vendor) VALUES (4444, 1, 'Sophos UTM', 'Sophos UTM remote logs', 26, 'Sophos');
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 3, NULL, NULL, 102, 'sophosutm: Generic UTM Event' ,3, 2);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 4, 6, 50, 124, 'sophosutm: IPS UDP flood Detected' ,4, 3);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 5, 6, 50, 124, 'sophosutm: IPS TCP SYN flood Detected' ,4, 3);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 6, 6, 50, 124, 'sophosutm: IPS ICMP flood Detected' ,4, 3);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 7, 7, 53, 123, 'sophosutm: IPS Portscan Detected' ,4, 3);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 8, 2, 24, 111, 'sophosutm: Authentication Succesfull' ,3, 2);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 9, 2, 24, 110, 'sophosutm: Authentication Failed' ,3, 2);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 10, 3, 75, NULL, 'sophosutm: Packet Filter Accept' ,3, 2);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 11, 3, 76, NULL, 'sophosutm: Packet Filter Reject' ,3, 2);
INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, 12, 3, 76, NULL, 'sophosutm: Packet Filter Drop' ,3, 2);
"""
for line in lines:
	line = line.strip()
	snortRule = parseRule(line)
	#print(snortRule)
	
	if "classtype" in snortRule:
		classtypesql = "(select id from classification where name = '%s')" % snortRule["classtype"]
		prioritysql = "4-(select priority from classification where name = '%s')" % snortRule["classtype"]
	else:
		classtypesql = "102"
		priority = '2'
	#print(classtypesql)
	
	sqlline = "INSERT INTO plugin_sid (plugin_id, sid, category_id, subcategory_id, class_id, name, priority, reliability) VALUES (4444, %s, 15, 172, %s, 'sophosutm: IPS %s' ,%s, 4);\n" % (snortRule["sid"], classtypesql, re.sub("group=\d+", "", snortRule["msg"]).strip()[2:].replace("\'", "\\\'"), prioritysql)
	
	sql = sql+sqlline
	#break

print("#==== sql\n%s" % sql)
