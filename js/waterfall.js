/* jshint asi:true */
//先等图片都加载完成
//再执行布局函数

/**
 * 执行主函数
 * @param  {[type]} function( [description]
 * @return {[type]}           [description]
 */
(function() {

  /**
     * 内容JSON
     */
  var demoContent = [
	  {
	      demo_link: 'http://192.168.1.12:8080/secure/Dashboard.jspa',
	      img_link: '/images/jira.png',
	      code_link: 'https://baike.baidu.com/item/JIRA',
	      title: 'Barry Bug\'s',
	      core_tech: '开源三方',
	      description: '工作中jira管理自己bug,个人bug管理主页'
	  }, {
      demo_link: 'http://192.168.80.2:8080/#/dashboard/self',
      img_link: '/images/gerrit.png',
      code_link: 'https://baike.baidu.com/item/Gerrit/3245666?fr=aladdin',
      title: 'gerrit工作代码提交',
      core_tech: '开源三方',
      description: '为公司代码提交通过审核页面。'
	  },{
      demo_link: 'http://bom.wheatek.com:8080/BomManagement/publicres/login.jsp',
      img_link: '/images/bom.jpg',
      code_link: '#',
      title: 'bom物料管理系统',
      core_tech: '公司内部系统',
      description: '为公司开发并维护bom系统。主要功能:工厂物料管理'
	  },{
      demo_link: 'http://fex.wheatek.com:8079/login.jsp',
      img_link: '/images/fex.jpg',
      code_link: '#',
      title: '文件外发系统',
      core_tech: '公司内部系统',
      description: '为公司维护push系统。主要功能:开发好的系统版本发给工厂量产'
	  },{
      demo_link: 'http://ota.wheatek.com:8604/padm/',
      img_link: '/images/push.jpg',
      code_link: '#',
      title: 'push系统',
      core_tech: '公司内部系统',
      description: '为公司开发并维护push系统。轮循推送apk'
	  },{
      demo_link: 'https://www.stubook.com.cn/HomeworkManagement/',
      img_link: '/images/stubook.jpg',
      code_link: '#',
      title: 'stubook学生平板',
      core_tech: '公司内部系统',
      description: '公司开发主要系统学生作业平板后台api'
	  },
	  {
      demo_link: 'http://gaohaoyang.github.io/ToDo-WebApp/',
      img_link: 'http://7q5cdt.com1.z0.glb.clouddn.com/blog-todoWebApp.png',
      code_link: 'https://github.com/Gaohaoyang/ToDo-WebApp',
      title: '百度前端学院 task0004 ToDo 应用(移动端)',
      core_tech: 'JavaScript LocalStorage requireJS Sass Gulp XSS',
      description: '在任务三中，做了一个 PC 端的 ToDo 应用。任务四是将它优化，以适应移动端设备。'
    }
  ];

  contentInit(demoContent) //内容初始化
  waitImgsLoad() //等待图片加载，并执行布局初始化
}());

/**
 * 内容初始化
 * @return {[type]} [description]
 */
function contentInit(content) {
  // var htmlArr = [];
  // for (var i = 0; i < content.length; i++) {
  //     htmlArr.push('<div class="grid-item">')
  //     htmlArr.push('<a class="a-img" href="'+content[i].demo_link+'">')
  //     htmlArr.push('<img src="'+content[i].img_link+'">')
  //     htmlArr.push('</a>')
  //     htmlArr.push('<h3 class="demo-title">')
  //     htmlArr.push('<a href="'+content[i].demo_link+'">'+content[i].title+'</a>')
  //     htmlArr.push('</h3>')
  //     htmlArr.push('<p>主要技术：'+content[i].core_tech+'</p>')
  //     htmlArr.push('<p>'+content[i].description)
  //     htmlArr.push('<a href="'+content[i].code_link+'">源代码 <i class="fa fa-code" aria-hidden="true"></i></a>')
  //     htmlArr.push('</p>')
  //     htmlArr.push('</div>')
  // }
  // var htmlStr = htmlArr.join('')
  var htmlStr = ''
  for (var i = 0; i < content.length; i++) {
    htmlStr += '<div class="grid-item">' + '   <a class="a-img" target ="_blank" href="' + content[i].demo_link + '">' + '       <img src="' + content[i].img_link + '">' + '   </a>' + '   <h3 class="demo-title">' + '       <a  target ="_blank"  href="' + content[i].demo_link + '">' + content[i].title + '</a>' + '   </h3>' + '   <p>主要技术：' + content[i].core_tech + '</p>' + '   <p>' + content[i].description + '       <a  target ="_blank" href="' + content[i].code_link + '">源代码 <i class="fa fa-code" aria-hidden="true"></i></a>' + '   </p>' + '</div>'
  }
  var grid = document.querySelector('.grid')
  grid.insertAdjacentHTML('afterbegin', htmlStr)
}

/**
 * 等待图片加载
 * @return {[type]} [description]
 */
function waitImgsLoad() {
  var imgs = document.querySelectorAll('.grid img')
  var totalImgs = imgs.length
  var count = 0
  //console.log(imgs)
  for (var i = 0; i < totalImgs; i++) {
    if (imgs[i].complete) {
      //console.log('complete');
      count++
    } else {
      imgs[i].onload = function() {
        // alert('onload')
        count++
        //console.log('onload' + count)
        if (count == totalImgs) {
          //console.log('onload---bbbbbbbb')
          initGrid()
        }
      }
    }
  }
  if (count == totalImgs) {
    //console.log('---bbbbbbbb')
    initGrid()
  }
}

/**
 * 初始化栅格布局
 * @return {[type]} [description]
 */
function initGrid() {
  var msnry = new Masonry('.grid', {
    // options
    itemSelector: '.grid-item',
    columnWidth: 250,
    isFitWidth: true,
    gutter: 20
  })
}
