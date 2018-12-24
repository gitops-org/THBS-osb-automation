package com.journaldev.spring.service;

import java.util.List;

import com.journaldev.hibernate.entity.Role;
import com.journaldev.hibernate.entity.User;

public interface UserWizardService {

	public void register(User user) throws Exception;

	public List<User> getUsersList() throws Exception;
	
	public List<Role> getRoleList() throws Exception;
	
	public void saveRole(Role role) throws Exception;

	public void deleteUser(User user)throws Exception;

	public void deleteRole(Role role)throws Exception;
	

}
