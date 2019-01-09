package com.ragsInfo.daoImpl;

import java.util.List;

import org.hibernate.Criteria;
import org.hibernate.FetchMode;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.ragsInfo.dao.ReportDao;
import com.ragsInfo.entity.Report;

@Repository
public class ReportDaoImpl implements ReportDao{
	@Autowired
	private SessionFactory sessionFactory;

	public SessionFactory getSessionFactory() {
		return sessionFactory;
	}

	public void setSessionFactory(SessionFactory sessionFactory) {
		this.sessionFactory = sessionFactory;
	}

	@Override
	@Transactional
	public List<Report> getReportsList() throws Exception {
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(Report.class,"report");
		List<Report> reports = cr.list();
		return reports;
	}

}
