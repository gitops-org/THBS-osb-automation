/**
 * 
 */
package com.javatpoint;

/**
 * @author girish_mohan
 *
 */
public class AGLogBean {

	private String soaTransactionID;
	private String agLogTime;
	private String processName;
	private float responseTime;
	private String serviceName;
	private String operationName;
	
	public String getSoaTransactionID() {
		return soaTransactionID;
	}
	public void setSoaTransactionID(String soaTransactionID) {
		this.soaTransactionID = soaTransactionID;
	}
	public String getAgLogTime() {
		return agLogTime;
	}
	public void setAgLogTime(String agLogTime) {
		this.agLogTime = agLogTime;
	}
	public String getProcessName() {
		return processName;
	}
	public void setProcessName(String processName) {
		this.processName = processName;
	}
	public float getResponseTime() {
		return responseTime;
	}
	public void setResponseTime(float responseTime) {
		this.responseTime = responseTime;
	}
	public String getServiceName() {
		return serviceName;
	}
	public void setServiceName(String serviceName) {
		this.serviceName = serviceName;
	}
	public String getOperationName() {
		return operationName;
	}
	public void setOperationName(String operationName) {
		this.operationName = operationName;
	}
	
}
