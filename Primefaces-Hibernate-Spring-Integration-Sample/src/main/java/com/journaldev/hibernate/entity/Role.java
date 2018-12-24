package com.journaldev.hibernate.entity;
// Generated Dec 14, 2018 12:43:04 PM by Hibernate Tools 5.3.0.Beta2

/**
 * Role generated by hbm2java
 */
public class Role implements java.io.Serializable {

	private int roleId;
	private String roleName;
	
	private String desc;


	public String getDesc() {
		return desc;
	}

	public void setDesc(String desc) {
		this.desc = desc;
	}

	public Role() {
	}

	public Role(int roleId, String roleName) {
		this.roleId = roleId;
		this.roleName = roleName;
	}


	public Role(String roleName) {
		this.roleName = roleName;
	}

	public int getRoleId() {
		return this.roleId;
	}

	public void setRoleId(int roleId) {
		this.roleId = roleId;
	}

	public String getRoleName() {
		return this.roleName;
	}

	public void setRoleName(String roleName) {
		this.roleName = roleName;
	}

}
