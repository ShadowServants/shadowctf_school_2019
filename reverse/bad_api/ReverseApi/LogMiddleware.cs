using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace ReverseApi
{
    public class LogMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<LogMiddleware> _log;

        public LogMiddleware(RequestDelegate next, ILogger<LogMiddleware> logger)
        {
            _next = next;
            _log = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            await _next.Invoke(context);
            var ip = context.Connection.RemoteIpAddress;
            var method = context.Request.Method;
            var status = context.Response.StatusCode;
            var route = context.Request.Path;
            _log.Log(LogLevel.Information, $"{ip} {method} {route} {status}");
        }
    }
}