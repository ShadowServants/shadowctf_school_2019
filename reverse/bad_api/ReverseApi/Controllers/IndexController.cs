using System.Text;
using Microsoft.AspNetCore.Mvc;

namespace ReverseApi.Controllers
{
    [Route("/")]
    [ApiController]
    public class IndexController : Controller
    {
        // GET
        [HttpGet]
        [HttpGet("{page}")]
        public IActionResult Index(string page = "index.html")
        {
            if (!System.IO.File.Exists("Files/" + page))
            {
                return NotFound("Page not found");
            }
            var sb = new StringBuilder(0);
            using (var sr = System.IO.File.OpenText("Files/" + page))
            {
                
                string s;
                while ((s = sr.ReadLine()) != null)
                {
                    sb.Append(s);
                }
                
            } 
            if (sb.Length == 0)
            {
                return NotFound("Page not found");
            }

            return Content(sb.ToString(), "text/html");
            
        }
    }
}