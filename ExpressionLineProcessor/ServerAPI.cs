using System;
using System.IO;
using System.Threading;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Web;
using System.Reflection;
using System.Net.Http.Headers;


namespace ServerAPI {

    public class MicroService {
        private string url_get, url_post;
        protected bool persistentMode;

        private HttpClient client = new() {
            Timeout = TimeSpan.FromSeconds(60)
        };

        public MicroService(string get_url, string post_url, bool persistentConnections = false) {
            url_get = get_url;
            url_post = post_url;
            persistentMode = persistentConnections;
        }

        public bool PersistentConnections { get { return persistentMode; } set { persistentMode = value; } }

        public T GetJob<T>(string job_type, out ResponseAddress address) {
            T content = RequestJob<T>("?type=" + HttpUtility.UrlEncode(job_type), out BasicContent recv);
            address = new ResponseAddress(recv.id, recv.visibleId);
            return content;
        }

        public T GetJob<T>(string job_type, string job_id) {
            return RequestJob<T>("?type=" + HttpUtility.UrlEncode(job_type) + "&id=" + HttpUtility.UrlEncode(job_id), out _);
        }

        public string GetJob<T>(string job_id, out T content) {
            content = RequestJob<T>("?id=" + HttpUtility.UrlEncode(job_id), out BasicContent recv);
            return recv.type;
        }

        private T RequestJob<T>(string request_str, out BasicContent received) {
            HttpResponseMessage response;
            Task<HttpResponseMessage> tresponse;
            while (true) {
                tresponse = client.GetAsync(url_get + request_str);
                try {
                    tresponse.Wait();
                    response = tresponse.Result;
                } catch {
                    if (tresponse.IsCanceled || persistentMode)
                        continue;
                    else
                        throw;
                }
                if (response.StatusCode != System.Net.HttpStatusCode.RequestTimeout)
                    break;
            }

            string rawcontent;
            using (var reader = new StreamReader(response.Content.ReadAsStream(), Encoding.UTF8)) {
                rawcontent = reader.ReadToEnd();
            }

            received = JsonSerializer.Deserialize<BasicContent>(rawcontent, JSON_SERIZLIZER_OPTIONS);
            T content = JsonSerializer.Deserialize<T>(((JsonElement)received.content).GetRawText(), JSON_SERIZLIZER_OPTIONS);

            return content;
        }

        public void PostFinalResult<T>(string result_type, ResponseAddress targetAddress, T content) {
            PostJob<T>(result_type, targetAddress.id, true, content);
        }

        public void PostIntermediateResult<T>(string result_type, ResponseAddress targetAddress, T content) {
            PostJob<T>(result_type, targetAddress.id, targetAddress.visibleId, content);
        }

        public void PostJob<T>(string job_type, T content) {
            PostJob<T>(job_type, "null", true, content);
        }

        public void PostJob<T>(string job_type, string job_id, bool visibleId, T content) {
            if (job_type == null) job_type = "null";

            BasicContent bcontent = new(job_type, job_id, visibleId, content);

            byte[] json = JsonSerializer.SerializeToUtf8Bytes(bcontent, JSON_SERIZLIZER_OPTIONS);

            HttpContent hcontent = new ByteArrayContent(json);

            Task<HttpResponseMessage> tresponse = null;

            while (true) {
                try {
                    tresponse = client.PostAsync(url_post, hcontent);
                    tresponse.Wait();
                    break;
                } catch {
                    if (!persistentMode)
                        throw;
                }
            }
        }

        public O ProcessAsFunction<O, I>(string requested_function, I content) {
            string cid = Assembly.GetExecutingAssembly().Location + "." + DateTime.UtcNow.Ticks.ToString() + "." + Thread.CurrentThread.ManagedThreadId.ToString();

            PostJob<I>(requested_function, cid, false, content);
            GetJob<O>(cid, out O result);
            return result;
        }

        public O ProcessAsFunction<O, I>(string requested_function, I content, string target_content_type) {
            string cid = Assembly.GetExecutingAssembly().Location + "." + DateTime.UtcNow.Ticks.ToString() + "." + Thread.CurrentThread.ManagedThreadId.ToString();

            PostJob<I>(requested_function, cid, false, content);
            return GetJob<O>(target_content_type, cid);
        }

        private static readonly JsonSerializerOptions JSON_SERIZLIZER_OPTIONS = new(JsonSerializerDefaults.Web) {
            IncludeFields = true
        };
        
        private class BasicContent {
            public BasicContent(string type, string id, bool visibleId, object content) {
                this.type = type;
                this.id = id;
                this.content = content;
                this.visibleId = visibleId;
            }

            public string id { get; set; }

            public bool visibleId { get; set; }

            public string type { get; set; }

            public object content { get; set; }
        }
    }

    public struct ResponseAddress {
        public string id;
        public bool visibleId;
        public ResponseAddress(string id, bool visibleId) {
            this.id = id; this.visibleId = visibleId;
        }
    }
}
