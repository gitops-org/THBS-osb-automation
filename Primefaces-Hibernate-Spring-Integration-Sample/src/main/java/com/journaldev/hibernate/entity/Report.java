package com.journaldev.hibernate.entity;
// Generated Jan 7, 2019 3:21:55 PM by Hibernate Tools 5.3.0.Beta2

/**
 * Report generated by hbm2java
 */
public class Report implements java.io.Serializable {

	private Integer reportId;
	private String oppId;
	private String campaignName;
	private Integer valueItem;
	private String ae;
	private String am;
	private Integer year;
	private String month;
	private Integer finalTotal;
	private Integer remaining;
	private Integer subtotal;

	public Report() {
	}

	public Report(String oppId, String campaignName, Integer valueItem, String ae, String am, Integer year,
			String month, Integer finalTotal, Integer remaining, Integer subtotal) {
		this.oppId = oppId;
		this.campaignName = campaignName;
		this.valueItem = valueItem;
		this.ae = ae;
		this.am = am;
		this.year = year;
		this.month = month;
		this.finalTotal = finalTotal;
		this.remaining = remaining;
		this.subtotal = subtotal;
	}

	public Integer getReportId() {
		return this.reportId;
	}

	public void setReportId(Integer reportId) {
		this.reportId = reportId;
	}

	public String getOppId() {
		return this.oppId;
	}

	public void setOppId(String oppId) {
		this.oppId = oppId;
	}

	public String getCampaignName() {
		return this.campaignName;
	}

	public void setCampaignName(String campaignName) {
		this.campaignName = campaignName;
	}

	public Integer getValueItem() {
		return this.valueItem;
	}

	public void setValueItem(Integer valueItem) {
		this.valueItem = valueItem;
	}

	public String getAe() {
		return this.ae;
	}

	public void setAe(String ae) {
		this.ae = ae;
	}

	public String getAm() {
		return this.am;
	}

	public void setAm(String am) {
		this.am = am;
	}

	public Integer getYear() {
		return this.year;
	}

	public void setYear(Integer year) {
		this.year = year;
	}

	public String getMonth() {
		return this.month;
	}

	public void setMonth(String month) {
		this.month = month;
	}

	public Integer getFinalTotal() {
		return this.finalTotal;
	}

	public void setFinalTotal(Integer finalTotal) {
		this.finalTotal = finalTotal;
	}

	public Integer getRemaining() {
		return this.remaining;
	}

	public void setRemaining(Integer remaining) {
		this.remaining = remaining;
	}

	public Integer getSubtotal() {
		return this.subtotal;
	}

	public void setSubtotal(Integer subtotal) {
		this.subtotal = subtotal;
	}

}
