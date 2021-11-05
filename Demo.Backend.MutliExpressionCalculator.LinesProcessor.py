import ServerAPI

serv = ServerAPI.MicroService(url_get='http://localhost:8080/got',
                                   url_post='http://localhost:8080/gave',
                                   persistentMode=True)

while True:
    data,addr = serv.GetNextJob(job_type='Demo.Backend.MutliExpressionCalculator.LinesProcessor')

    for i in range(0, len(data)):
        data[i] = serv.ProcessAsFunction(content=data[i],
                           requested_function='Demo.Backend.ExpressionLineProcessjor.Handle',
                           target_content_type='Demo.Backend.ExpressionLineProcessor.Output')

    serv.PostFinalResult(content=data,
                         result_type='Demo.Backend.MutliExpressionCalculator.ResultingLines',
                         responseAddress=addr)
