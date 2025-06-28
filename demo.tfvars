tmac-internet = {
    app_rules = {
        tsac_all ={
            env   = ["dev", "int", "prod"]
            protocols = ["Https", 443]
            fqdns = [
                "abc.com" # added abc
                "xyz.com" # added xyz
                "added.com", #added
                "test001.com", test001
                "test002.com", # test002 added
                "test003.com", # test003 added 
            ]
        }
    }
}

mishra = {
    app_rules = {
        abinash_all = {}
        env = ["dev", "int"]
        prtocols = [["Https", 443]]
        fqdns = [
            "happy.com",

        ]
    }
}
