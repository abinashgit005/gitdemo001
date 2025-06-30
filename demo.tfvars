tmac-internet = {
    app_rules = {
        tsac_all ={
            env   = ["dev", "int", "prod"]
            protocols = ["Https", 443]
            fqdns = [
                "abc.com" # added abc
                "xyz.com" # added xyz
                "added.com", #added
                "update.com", # update
                "amazon.com",   # amazon added
                "again.com",   # added again
                "ghi.com",   # ghi added
                "aka.com",    # aka added 
                "okay.com" # added okay
                "gcp.com"   # added gcp for test
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
