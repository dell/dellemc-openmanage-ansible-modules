create template.:
{
    "changed": true,
    "msg": "Successfully created a template with ID 123",
    "return_id": 123
}


modify template.:
{
    "changed": true,
    "msg": "Successfully modified the template with ID 123",
    "return_id": 123
}


deploy template.:
{
    "changed": true,
    "msg": "Successfully created the template-deployment job with ID 456",
    "return_id": 456
}

delete template:
{
    "changed": true,
    "msg": "Successfully deleted the template",
}

import xml:
{
    "changed": true,
    "msg": "Successfully imported the xml and created template with ID 48",
    "return_id": 48
}

clone template:
{
    "changed": true,
    "msg": "Successfully cloned the template and created template with ID 47",
    "return_id": 47
}

export template:
 {
    "changed": false,
    "Content": "<SystemConfiguration Model=\"PowerEdge R940\" ServiceTag=\"DG22TR2\" 
    TimeStamp=\"Tue Sep 24 09:20:57.872551 2019\">\n<Component FQDD=\"AHCI.Slot.6-1\">\n<Attribute 
    Name=\"RAIDresetConfig\">True</Attribute>\n<Attribute Name=\"RAIDforeignConfig\">Clear</Attribute>\n
    </Component>\n<Component FQDD=\"Disk.Direct.0-0:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDHotSpareStatus\">No
    </Attribute>\n<Attribute Name=\"RAIDPDState\">Ready</Attribute>\n</Component>\n
    <Component FQDD=\"Disk.Direct.1-1:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDHotSpareStatus\">No
    </Attribute>\n<Attribute Name=\"RAIDPDState\">Ready</Attribute>\n</Component>\n</SystemConfiguration>\n",
    "ContentType": "xml",
    "TemplateId": 42,
    "ViewTypeId": 2,
    "msg": "Successfully exported the template"
}
