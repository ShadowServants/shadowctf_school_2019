using Microsoft.AspNetCore.Mvc;

namespace ReverseApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlagController : ControllerBase
    {
        [HttpGet]
        public ActionResult<string> Get()
        {
            return "No flag for you";
        }


        [HttpPost]
        public ActionResult<string> Post()
        {
            var ip = Request.HttpContext.Connection.RemoteIpAddress.ToString();
            var hash = Crypto.GetHash(Crypto.Reverse(Crypto.GetHash(ip)));

            var f = Request.Headers["X-Flag"];
            return Content(Crypto.XorStrings(hash, f) != "373C855211F1916314B3225A6CF7381525F3614E40" ? "BAD FLAG" : "GOOD FLAG BRO!");
        }
    }
}