package db;

public class PagerInfo {
	public static final int DEFAULT_PAGESIZE = 10;
	public static final int DEFAULT_PAGEINDEX = 1;
	private Integer pageCount; //总共多少页
	private Integer pageSize = DEFAULT_PAGESIZE; //每页显示多少条
	private Integer pageIndex = DEFAULT_PAGEINDEX; //当前第几页
	private Integer recordCount; //总共有多少条记录
	
	public Integer getPageCount() {
		return pageCount;
	}
	public Integer getPageSize() {
		return pageSize;
	}
	public void setPageSize(Integer pageSize) {
		this.pageSize = pageSize;
	}
	public Integer getPageIndex() {
		return pageIndex;
	}
	public void setPageIndex(Integer pageIndex) {
		if(pageIndex<=0) {
			pageIndex = DEFAULT_PAGEINDEX;
		}
		this.pageIndex = pageIndex;
	}
	public Integer getRecordCount() {
		return recordCount;
	}
	public void setRecordCount(Integer recordCount) {
		this.recordCount = recordCount;
		pageCount = recordCount%pageSize==0 ? recordCount/pageSize : recordCount/pageSize+1;
		if(pageIndex>pageCount && pageCount>0) {
			pageIndex = pageCount;
		}
	}
	/**
	 * 如果每页显示10条，显示第2页就是显示11-20条记录
	 * 如果要显示11-20条记录，那么startRecord返回10
	 * @return
	 */
	public Integer getStartRecord() {
		return pageSize*(pageIndex-1);
	}
}
