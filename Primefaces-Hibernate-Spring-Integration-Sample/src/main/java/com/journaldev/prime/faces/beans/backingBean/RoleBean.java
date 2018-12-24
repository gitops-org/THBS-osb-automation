package com.journaldev.prime.faces.beans.backingBean;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;

import org.springframework.stereotype.Controller;

@ManagedBean(name="roleBean",eager=true)
@RequestScoped
@Controller
public class RoleBean {

	private String roleName;
	private String desc;

	public String getDesc() {
		return desc;
	}

	public void setDesc(String desc) {
		this.desc = desc;
	}


	public String getRoleName() {
		return this.roleName;
	}

	public void setRoleName(String roleName) {
		this.roleName = roleName;
	}

		
		
}