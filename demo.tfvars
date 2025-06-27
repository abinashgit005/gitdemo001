tmac-internet = {
    app_rules = {
        tsac_all ={
            env   = ["dev", "int", "prod"]
            protocols = ["Https", 443]
            fqdns = [
                abc.com # added abc
                xyz.com # added xyz
                "mno.com",   # added mno
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
