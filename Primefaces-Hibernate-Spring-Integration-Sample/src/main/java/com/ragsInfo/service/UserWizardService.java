package com.ragsInfo.service;

import java.util.List;

import com.ragsInfo.entity.Role;
import com.ragsInfo.entity.Tagging;
import com.ragsInfo.entity.User;

public interface UserWizardService {

	public void register(User user) throws Exception;

	public List<User> getUsersList() throws Exception;
	
	public List<Role> getRoleList() throws Exception;
	
	public void saveRole(Role role) throws Exception;

	public void deleteUser(User user)throws Exception;

	public void deleteRole(Role role)throws Exception;

	public List<Tagging> getTaggingList()throws Exception;

	public void saveTagging(Tagging tag) throws Exception;

	public void deleteTagging(Tagging tag) throws Exception;
	

}
