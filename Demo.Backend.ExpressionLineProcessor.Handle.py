import ServerAPI

serv = ServerAPI.MicroService(url_get='http://localhost:8080/got',
                                   url_post='http://localhost:8080/gave',
                                   persistentMode=True)

while True:
    data,addr = serv.GetNextJob(job_type='Demo.Backend.ExpressionLineProcessor.Handle')

    try:
        data = eval(data)
    except:
        data = f"Выражение '{str(data)}' некорректно"

    serv.PostFinalResult(content=data,
                         result_type='Demo.Backend.ExpressionLineProcessor.Output',
                         responseAddress=addr)
