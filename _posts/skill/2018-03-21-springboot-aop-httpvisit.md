---
layout: post
title: spring aop 记录请求日志
category: 技术
tags:  概率 增长率 留存率 mysql
keywords: mysql rate
description: 2018-01-10-redis-nginx.md
---


* content
{:toc}




## 业务监控

> 为了查询请求log ,建议加一个对请求响应的日志记录,让后定时清理数据





## 记录日志

``` java 

/**
 * 拦截某些敏感操作记录到数据库
 * @author BarryLiu
 *
 */
@Aspect
@Component
public class HttpAspect {
	public static Logger logger = LoggerFactory.getLogger(HttpAspect.class);
	
	@Autowired
	private VisitService visitService;

	/**
	 * 配置切面
	 */
//	@Pointcut("execution (public * com.wheatek.push.controller.MsgController.sync(..))")
	@Pointcut("execution (public * com.wheatek.push.controller.*.*(..))")
	public void log() {}
	
	
	/**
     * 可以在执行方法之前和之后改变参数和返回值
     * @param joinPoint用于获取目标方法相关信息的参数
     * @return 最终的返回值
     * @throws Throwable
     */
	@Around("log()")
    public Object processTx(ProceedingJoinPoint joinPoint) throws Throwable {
		
		
		ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
		HttpServletRequest request = attributes.getRequest();
		String requestUrl = request.getRequestURL().toString();
		if(requestUrl.endsWith("/api")||requestUrl.endsWith("/agent")) {
			//是请求的  /api ,RsaController 或/agent AgentController 下面api接口,转发的要忽略, @Pointcut 切的时候把所有的controller都切进去啦
			  Object rvt = joinPoint.proceed();
			  return rvt;
		}else {
			
	//		Object[] args = joinPoint.getArgs();
	//		int fromVal = HttpUtil.getFromVal(request);
			String requestBody = HttpUtil.getRequestBody(request);
			String ip = HttpUtil.getClientIP(request);

			System.out.println("Around ：执行方法之前 ");
			
	       long startTime = System.currentTimeMillis();
	        //执行 controller方法
	        Object rvt = joinPoint.proceed();
	        
	        long duration = System.currentTimeMillis() - startTime;
	        String responseBody = rvt.toString();
	        if(responseBody.indexOf("forward:")>-1) { //内部转发不需要打log
	        	return rvt;
	        }
	        
	        System.out.println("Around ：执行方法之后");
	        String uuid =null;
	        try {//取的到uuid就取,取不到就算了
	        	if (requestUrl.indexOf("/msg/sync") > 0) {//调用getMsg接口 要取得其uuid保存
		        	JSONObject json = HttpUtil.formatData(request);
		        	JSONObject details = json.getJSONObject("details");
		        	if(details!=null) {
		        		uuid = details.getString("uuid");
		        	}
		        } else {//都取一下uuid吧
		        	JSONObject json = HttpUtil.formatData(request);
		        	JSONObject details = json.getJSONObject("details");
		        	if(details!=null) {
		        		uuid = details.getString("uuid");
		        	}
				}
	        }catch(Exception e) {
	        	System.out.println("取不到uuid.......");
	        }
	        
	        
	     // isEnc 是 RsaController解密后转发到其它Controller带的开关,如果有并且 equals("t"),返回也需要加密,   如果有加过密的就不用再加密啦
	     	String isEnc = HttpUtil.getString(request, "isEnc","f");
			saveVisit(uuid,duration,ip,requestUrl,"isEnc="+isEnc+"&"+requestBody,responseBody);
			
			if(isEnc!=null&&"t".equals(isEnc)||requestUrl.indexOf("msg/pushMsgBin")>-1) {//客户端加密,  
				RsaBean encKey = RsaSimpleUtils.getRandomPriRsaKeys(RsaSimpleUtils.PUBKEY);
				String index = encKey.getIndex();// 传index
				int[] encrypt = RsaSimpleUtils.encrypt(responseBody, encKey.getPublicKey(), encKey.getN());

				/*StringBuffer sb = new StringBuffer();
				sb.append("{\"code\":\"00\",\"id\":\""+index+"\",\"details\":\""+Arrays.toString(encrypt)+"\"}");
				return sb.toString();*/
				RsaRes rsaRes = new RsaRes();
				rsaRes.setId(index);
				rsaRes.setDetails(Arrays.toString(encrypt));
				return JSON.toJSONString(rsaRes);
			}
	        return rvt;
		}
    }

	/**
     * 可以在执行方法之前对目标方法的参数进行判断
     * 通过抛出一个异常来阻断目标方法的访问
     * @param joinPoint
     */
	@Before("log()")
	public void toLog(JoinPoint joinpoint) {
//		logger.info("....");

	}
	
	/**
     * 可以在执行方法之后对目标方法的参数进行判断
     * @param joinPoint
     */
	@After("log()")
	public void afterLog(JoinPoint joinPoint) {
//		System.out.println("afterLog");
	}
	
	/**
     * 与After的区别在于AfterReturning只有在方法执行成功的之后才会被织入，如果After和
     * AfterReturning同时存在于一个文件中，谁写在前面谁先运行
     * @param joinPoint
     * @param object方法的返回值
     */
	@AfterReturning(returning="object",pointcut="log()")
	public void afterReturnLog(JoinPoint joinPoint,Object object) {
//		System.out.println("afterReturning");
	}
	
	private void saveVisit(String uuid,long duration,String ip,String requestUrl,String requestBody,String responseBody) {
		Visit visit = new Visit();
		try {
			if (requestUrl.indexOf("http://localhost") != -1) {
				return;
			}
			visit.setUrl(requestUrl);
			visit.setRequestBody(requestBody);
			visit.setResponseBody(responseBody);
			visit.setIp(ip);
			visit.setUuid(uuid);
			visit.setDuration(duration);
			visitService.save(visit);
			logger.info("save visit succ："+visit.toString());
		} catch (Exception e) {
			logger.error("save visit error : "+visit.toString()+"" + e.getMessage());
		}
	}
}
 
```