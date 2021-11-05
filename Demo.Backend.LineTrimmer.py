import ServerAPI

serv = ServerAPI.MicroService(url_get='http://localhost:8080/got',
                                   url_post='http://localhost:8080/gave',
                                   persistentMode=True)

while True:
    data,addr = serv.GetNextJob(job_type='Demo.Backend.LineTrimmer')

    lines = [w.strip() for w in data]
    data = [w for w in lines if w]

    serv.PostFinalResult(content=data,
                         result_type='Demo.Backend.LineTrimmer.Result',
                         responseAddress=addr)
