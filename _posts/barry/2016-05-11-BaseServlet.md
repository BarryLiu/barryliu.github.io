package com.ragentek.project.servlet;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

 
public class BaseServlet extends HttpServlet {

    public final String KEY_OP = "op";
    public static String OP_NAME;

    public static final String OP_QUERY = "query";
    public static final String OP_GET = "get";
    public static final String OP_ADD = "add";
    public static final String OP_DELETE = "delete";
    public static final String OP_UPDATE = "update";
    public static final String OP_OTHER = "other";

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        resp.setContentType("text/html;charset=UTF-8;pageEncoding=UTF-8");
        System.out.println("op=" + req.getParameter(KEY_OP));
        OP_NAME = req.getParameter(KEY_OP);
        OP_NAME = StringTools.isEmpty(OP_NAME) ? OP_QUERY : OP_NAME;
        if (OP_QUERY.equals(OP_NAME)) {
            query(req, resp);
        } else if (OP_GET.equals(OP_NAME)) {
            get (req, resp);
        } else if (OP_ADD.equals(OP_NAME)) {
            add (req, resp);
        } else if (OP_DELETE.equals(OP_NAME)) {
            delete(req, resp);
        } else if (OP_UPDATE.equals(OP_NAME)) {
            update(req, resp);
        } else if (OP_OTHER.equals(OP_NAME)) {
            other (req, resp);
        }
    }


    /**
     * 子类重写用于做查询操作，默认的动作
     *
     * @param req
     * @param resp
     * @throws ServletException
     * @throws IOException
     */
    protected void query(HttpServletRequest req,
                                  HttpServletResponse resp) throws ServletException, IOException{

    }

    /**
     * 请求参数包含：operation=update 时调用 子类重写用于更新数据
     *
     * @param req
     * @param resp
     * @throws ServletException
     * @throws IOException
     */
    protected void update(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
    }

    /**
     * 请求参数包含：operation=delete 时调用 子类重写用于删除数据
     *
     * @param req
     * @param resp
     * @throws ServletException
     * @throws IOException
     */
    protected void delete(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
    }

    /**
     * 请求参数包含：operation=add 时调用 子类重写用于添加数据
     *
     * @param req
     * @param resp
     * @throws ServletException
     * @throws IOException
     */
    protected void add(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
    }

    /**
     * 请求参数包含：operation=add 时调用 子类重写用于添加数据
     *
     * @param req
     * @param resp
     * @throws ServletException
     * @throws IOException
     */
    protected void get(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
    }

    /**
     * 请求参数包含：operation=other 时调用 子类重写用于添加数据
     *
     * @param req
     * @param resp
     * @throws ServletException
     * @throws IOException
     */
    protected void other(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
    }
}
