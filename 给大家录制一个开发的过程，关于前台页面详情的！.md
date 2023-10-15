给大家录制一个开发的过程，关于前台页面详情的！

1. 希望大家认真学习！
2. 注意springboot的使用！
3. 首先我们先进入我们的前端吧！

http://localhost:8081/#/detail/29

我们来分析下这个跳转到我们前端商品详情页面的地址，用restful接口可以写：

http://localhost:8081/#/detail/{id}

然后我们看看它给后端发了那些axios，也就是所谓的ajax异步请求

D:\Projects\前端—前台\tulingmall-front\src\pages\detail.vue

这个vue文件就说明了这一点，我们就挂这个vue到页面上去

```htaccess
    getProductInfo() {
      this.axios.get(`/product/detail/${this.id}`).then((res) => {
      //这就是前端商品详情的axios请求
        this.product = res;
        this.albumPics = res.albumPics.split(",");
        this.albumPics.unshift(res.pic);
        if (
          this.albumPics == null ||
          this.albumPics == undefined ||
          this.albumPics == ""
        ) {
          this.albumPics = res.pic.split(",");
        }
        this.serviceIds = res.serviceIds.split(",");
      });
    },
```

下面去后端创建我们的controller来实现我们前端的请求

productController：

```java
package com.tulingxueyuan.mall.controller;
import com.tulingxueyuan.mall.common.api.CommonResult;
import com.tulingxueyuan.mall.modules.pms.service.PmsProductService;
import com.tulingxueyuan.mall.dto.ProductDetailDTO;
import io.swagger.annotations.Api;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
@RestController
@Api(tags = "ProductController",description = "商品详情服务接口")
@RequestMapping("/product")
public class ProductController {
    @Autowired
    PmsProductService productService;
    /**
     *  取商品详情获
     * .get(`/product/detail/${this.id}`)
     */
    @RequestMapping("/detail/{id}")
    public CommonResult getProductDetail(@PathVariable Long id){
        //pojo不能满足我们的需求，我们需要一个dto，也就是对象传输单元来传输我商品的数据
        ProductDetailDTO productDetailDTO= productService.getProductDetail(id);
        return CommonResult.success(productDetailDTO);
    }
}

```

productDTO:

```java
package com.tulingxueyuan.mall.controller;
import com.tulingxueyuan.mall.common.api.CommonResult;
import com.tulingxueyuan.mall.modules.pms.service.PmsProductService;
import com.tulingxueyuan.mall.dto.ProductDetailDTO;
import io.swagger.annotations.Api;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
@RestController
@Api(tags = "ProductController",description = "商品详情服务接口")
@RequestMapping("/product")
public class ProductController {
    @Autowired
    PmsProductService productService;//默认已经实现了在service的impl文件下实现了所有接口
    /**
     *  取商品详情获
     * .get(`/product/detail/${this.id}`)
     */
    @RequestMapping("/detail/{id}")
    public CommonResult getProductDetail(@PathVariable Long id){
        //注意这里是点击某一个商品的详情，所以大家要注意下
        ProductDetailDTO productDetailDTO= productService.getProductDetail(id);
        return CommonResult.success(productDetailDTO);
    }
}

```

接口=>mapper接口下面就来到productDTO的mapper接口下：

productMapperDTO

```java
package com.tulingxueyuan.mall.modules.pms.mapper;
import com.tulingxueyuan.mall.modules.pms.model.PmsProduct;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.tulingxueyuan.mall.dto.ProductDetailDTO;

/**
 * <p>
 * 商品信息 Mapper 接口
 * </p>
 *
 */
public interface PmsProductMapper extends BaseMapper<PmsProduct> {
    ProductDetailDTO getProductDetail(Long id);
}

```

它实现了吗？

```java
package com.tulingxueyuan.mall.modules.pms.service.impl;

import com.tulingxueyuan.mall.modules.pms.model.PmsProduct;
import com.tulingxueyuan.mall.modules.pms.mapper.PmsProductMapper;
import com.tulingxueyuan.mall.dto.ProductDetailDTO;
import com.tulingxueyuan.mall.modules.pms.service.PmsProductService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * <p>
 * 商品信息 服务实现类
 * </p>
 */
@Service
public class PmsProductServiceImpl extends ServiceImpl<PmsProductMapper, PmsProduct> implements PmsProductService {
//他总共实现了两个泛型参数的传递，和一个业务层接口的继承实现
    @Autowired
    PmsProductMapper productMapper;

    /**
     * 取商品详情获
     * @param id 商品id
     * @return
     */

    public ProductDetailDTO getProductDetail(Long id) {
        return productMapper.getProductDetail(id);
    }
}

```

显然实现了接口，定义了接口实现的方法    @Override说明重写了

productService：

```java
package com.tulingxueyuan.mall.modules.pms.service;
import com.tulingxueyuan.mall.modules.pms.model.PmsProduct;
import com.baomidou.mybatisplus.extension.service.IService;
import com.tulingxueyuan.mall.dto.ProductDetailDTO;

/**
 * <p>
 * 商品信息 服务类
 * </p>
 */
public interface PmsProductService extends IService<PmsProduct> {
    /**
     * 取商品详情获
     * @param id 商品id
     * @return
     */
    ProductDetailDTO getProductDetail(Long id);
}


```



PmsProduct:

```java
package com.tulingxueyuan.mall.modules.pms.model;

import java.math.BigDecimal;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.annotation.IdType;
import java.util.Date;
import com.baomidou.mybatisplus.annotation.TableId;
import java.io.Serializable;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * <p>
 * 商品信息
 * </p>
 *
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("pms_product")
@ApiModel(value="PmsProduct对象", description="商品信息")
public class PmsProduct implements Serializable {
//继承的泛型是一个序列化接口，用于保存所有的商品属性名
    private static final long serialVersionUID=1L;

    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    private Long brandId;

    private Long productCategoryId;

    private Long feightTemplateId;

    private Long productAttributeCategoryId;

    private String name;

    private String pic;

    @ApiModelProperty(value = "货号")
    private String productSn;

    @ApiModelProperty(value = "删除状态：0->未删除；1->已删除")
    private Integer deleteStatus;

    @ApiModelProperty(value = "上架状态：0->下架；1->上架")
    private Integer publishStatus;

    @ApiModelProperty(value = "新品状态:0->不是新品；1->新品")
    private Integer newStatus;

    @ApiModelProperty(value = "推荐状态；0->不推荐；1->推荐")
    private Integer recommandStatus;

    @ApiModelProperty(value = "审核状态：0->未审核；1->审核通过")
    private Integer verifyStatus;

    @ApiModelProperty(value = "排序")
    private Integer sort;

    @ApiModelProperty(value = "销量")
    private Integer sale;

    private BigDecimal price;

    @ApiModelProperty(value = "促销价格")
    private BigDecimal promotionPrice;

    @ApiModelProperty(value = "赠送的成长值")
    private Integer giftGrowth;

    @ApiModelProperty(value = "赠送的积分")
    private Integer giftPoint;

    @ApiModelProperty(value = "限制使用的积分数")
    private Integer usePointLimit;

    @ApiModelProperty(value = "副标题")
    private String subTitle;

    @ApiModelProperty(value = "商品描述")
    private String description;

    @ApiModelProperty(value = "市场价")
    private BigDecimal originalPrice;

    @ApiModelProperty(value = "库存")
    private Integer stock;

    @ApiModelProperty(value = "库存预警值")
    private Integer lowStock;
    @ApiModelProperty(value = "单位")
    private String unit;
    @ApiModelProperty(value = "商品重量，默认为克")
    private BigDecimal weight;
    @ApiModelProperty(value = "是否为预告商品：0->不是；1->是")
    private Integer previewStatus;
    @ApiModelProperty(value = "以逗号分割的产品服务：1->无忧退货；2->快速退款；3->免费包邮")
    private String serviceIds;

    private String keywords;

    private String note;
    @ApiModelProperty(value = "画册图片，连产品图片限制为5张，以逗号分割")
    private String albumPics;

    private String detailTitle;

    private String detailDesc;

    @ApiModelProperty(value = "产品详情网页内容")
    private String detailHtml;

    @ApiModelProperty(value = "移动端网页详情")
    private String detailMobileHtml;

    @ApiModelProperty(value = "促销开始时间")
    private Date promotionStartTime;

    @ApiModelProperty(value = "促销结束时间")
    private Date promotionEndTime;

    @ApiModelProperty(value = "活动限购数量")
    private Integer promotionPerLimit;

    @ApiModelProperty(value = "促销类型：0->没有促销使用原价;1->使用促销价；2->使用会员价；3->使用阶梯价格；4->使用满减价格；5->限时购")
    private Integer promotionType;

    @ApiModelProperty(value = "品牌名称")
    private String brandName;

    @ApiModelProperty(value = "商品分类名称")
    private String productCategoryName;
}
```

我们知道一个Mapper 接口会对应一个数据库的查询mapper文件的字段映射与查询，所以我们需要看下他是怎么查的？

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.tulingxueyuan.mall.modules.pms.mapper.PmsProductMapper">
    <!-- 通用查询映射结果 -->
    <resultMap id="BaseResultMap" type="com.tulingxueyuan.mall.modules.pms.model.PmsProduct">
        <id column="id" property="id" />
        <result column="brand_id" property="brandId" />
        <result column="product_category_id" property="productCategoryId" />
        <result column="feight_template_id" property="feightTemplateId" />
        <result column="product_attribute_category_id" property="productAttributeCategoryId" />
        <result column="name" property="name" />
        <result column="pic" property="pic" />
        <result column="product_sn" property="productSn" />
        <result column="delete_status" property="deleteStatus" />
        <result column="publish_status" property="publishStatus" />
        <result column="new_status" property="newStatus" />
        <result column="recommand_status" property="recommandStatus" />
        <result column="verify_status" property="verifyStatus" />
        <result column="sort" property="sort" />
        <result column="sale" property="sale" />
        <result column="price" property="price" />
        <result column="promotion_price" property="promotionPrice" />
        <result column="gift_growth" property="giftGrowth" />
        <result column="gift_point" property="giftPoint" />
        <result column="use_point_limit" property="usePointLimit" />
        <result column="sub_title" property="subTitle" />
        <result column="description" property="description" />
        <result column="original_price" property="originalPrice" />
        <result column="stock" property="stock" />
        <result column="low_stock" property="lowStock" />
        <result column="unit" property="unit" />
        <result column="weight" property="weight" />
        <result column="preview_status" property="previewStatus" />
        <result column="service_ids" property="serviceIds" />
        <result column="keywords" property="keywords" />
        <result column="note" property="note" />
        <result column="album_pics" property="albumPics" />
        <result column="detail_title" property="detailTitle" />
        <result column="detail_desc" property="detailDesc" />
        <result column="detail_html" property="detailHtml" />
        <result column="detail_mobile_html" property="detailMobileHtml" />
        <result column="promotion_start_time" property="promotionStartTime" />
        <result column="promotion_end_time" property="promotionEndTime" />
        <result column="promotion_per_limit" property="promotionPerLimit" />
        <result column="promotion_type" property="promotionType" />
        <result column="brand_name" property="brandName" />
        <result column="product_category_name" property="productCategoryName" />
    </resultMap>
    <resultMap id="ProductDetailMap" extends="BaseResultMap" type="com.tulingxueyuan.mall.dto.ProductDetailDTO">
        <!--商品的sku-->
        <collection property="skuStockList" columnPrefix="sku_" resultMap="com.tulingxueyuan.mall.modules.pms.mapper.PmsSkuStockMapper.BaseResultMap"></collection>
        <!--商品的spk-->
        <collection property="productAttributeValueList"  columnPrefix="att_" ofType="com.tulingxueyuan.mall.dto.PmsProductAttributeValueDTO" >
            <id column="id" property="id" />
            <result column="product_id" property="productId" />
            <result column="product_attribute_id" property="productAttributeId" />
            <result column="value" property="value" />
            <result column="attrname" property="attrName"></result>
        </collection>
    </resultMap>
   <select id="getProductDetail"  resultMap="ProductDetailMap">
        SELECT
        p.*,
        pc.parent_id cate_parent_id,
        p.brand_id,
        sku.id sku_id, sku.lock_stock sku_lock_stock, sku.low_stock sku_low_stock, sku.pic sku_pic,sku.price sku_price,sku.product_id sku_product_id,sku.promotion_price sku_promotion_price,sku.sale sku_sale,sku.sku_code sku_sku_code,sku.sp1 sku_sp1,sku.sp2 sku_sp2,sku.sp3 sku_sp3,sku.stock sku_stock,
        att.id att_id,att.product_attribute_id att_product_attribute_id,att.product_id att_product_id,att.value att_value,
				(SELECT pa.name FROM pms_product_attribute pa where pa.id =att.product_attribute_id) att_attrname
        FROM pms_product p
        -- 一级和二级分类id
        LEFT JOIN pms_product_category pc ON p.product_category_id=pc.id
        LEFT JOIN pms_sku_stock sku on sku.product_id=p.id
        LEFT JOIN pms_product_attribute_value att on att.product_id=p.id
        where p.id=#{id}
   </select>

</mapper>

```

![image-20231001204505342](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20231001204505342.png)

从sql的查询结果可以看明白，我们前端可以查询到的字段，这个sql是可以优化的，你们下去可以自己试试！

再看看前端的响应拦截器有没有拦截到我们的数据呢？

我们发现有两个拦截器：

```vue
// 接口错误拦截
axios.interceptors.response.use(function(response){ 
  let res = response.data;
  let path = location.hash;   

  if(res.code==undefined){
    return res;
  }

  // 处理CommonResult逻辑
  if(res.code == 200){
    return res.data;
  }else if(res.code==401 || res.code==403|| res.code==600){  //|| res.code==401 || res.code==403 
    if (path != '#/index'){
     
      window.location.href = '/#/login';
    }
    return Promise.reject(res);
  }else{
    Message.warning(res.message);
    return Promise.reject(res);
  }
},(error)=>{ 
  //可以自己定义错误回调
  // let res=error.response;Message.error(res.data.message);
  // 
  Message.error(error.message);
  return Promise.reject(error);
});
```

我们发现并没有出现我们的商品页面而且登录的session直接失效！！！

```
{"code":99999,"message":"未知异常，请稍后再试！","data":null}
```

我们竟然发现它返回了这个未知的异常！

果然是后端的数据出了问题，我们来看看服务器的日志信息：

我们来记录看下

```java
023-10-01 21:09:41.727 ERROR 12512 --- [io-8888-exec-10] c.t.m.c.e.GlobalExceptionHandler         : 运行时异常：

java.lang.NullPointerException: Cannot invoke "java.util.Map.get(Object)" because "map" is null
	at com.tulingxueyuan.mall.modules.oms.service.impl.OmsCartItemServiceImpl.getCarProdutSum(OmsCartItemServiceImpl.java:113) ~[classes/:na]
	at com.tulingxueyuan.mall.modules.oms.service.impl.OmsCartItemServiceImpl$$FastClassBySpringCGLIB$$d8b04ca9.invoke(<generated>) ~[classes/:na]
	at org.springframework.cglib.proxy.MethodProxy.invoke(MethodProxy.java:218) ~[spring-core-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:687) ~[spring-aop-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at com.tulingxueyuan.mall.modules.oms.service.impl.OmsCartItemServiceImpl$$EnhancerBySpringCGLIB$$d38d996.getCarProdutSum(<generated>) ~[classes/:na]
	at com.tulingxueyuan.mall.controller.CarController.getCarProdutSum(CarController.java:50) ~[classes/:na]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:578) ~[na:na]
	at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:190) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:138) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:105) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:878) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:792) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1040) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:943) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:898) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:626) ~[tomcat-embed-core-9.0.39.jar:4.0.FR]
	at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883) ~[spring-webmvc-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:733) ~[tomcat-embed-core-9.0.39.jar:4.0.FR]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53) ~[tomcat-embed-websocket-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:113) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:113) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at com.alibaba.druid.support.http.WebStatFilter.doFilter(WebStatFilter.java:123) ~[druid-1.1.10.jar:1.1.10]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:320) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.invoke(FilterSecurityInterceptor.java:126) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.doFilter(FilterSecurityInterceptor.java:90) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:118) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:137) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.authentication.AnonymousAuthenticationFilter.doFilter(AnonymousAuthenticationFilter.java:111) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:158) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.savedrequest.RequestCacheAwareFilter.doFilter(RequestCacheAwareFilter.java:63) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at com.tulingxueyuan.mall.security.config.component.JwtAuthenticationFilter.doFilterInternal(JwtAuthenticationFilter.java:73) ~[classes/:na]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:116) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.web.filter.CorsFilter.doFilterInternal(CorsFilter.java:92) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.header.HeaderWriterFilter.doHeadersAfter(HeaderWriterFilter.java:92) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.header.HeaderWriterFilter.doFilterInternal(HeaderWriterFilter.java:77) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:105) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter.doFilterInternal(WebAsyncManagerIntegrationFilter.java:56) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy.doFilterInternal(FilterChainProxy.java:215) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.security.web.FilterChainProxy.doFilter(FilterChainProxy.java:178) ~[spring-security-web-5.3.5.RELEASE.jar:5.3.5.RELEASE]
	at org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:358) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:271) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.springframework.boot.actuate.metrics.web.servlet.WebMvcMetricsFilter.doFilterInternal(WebMvcMetricsFilter.java:93) ~[spring-boot-actuator-2.3.6.RELEASE.jar:2.3.6.RELEASE]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.11.RELEASE.jar:5.2.11.RELEASE]
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:202) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:542) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:143) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:374) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:868) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1590) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1144) ~[na:na]
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:642) ~[na:na]
	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61) ~[tomcat-embed-core-9.0.39.jar:9.0.39]
	at java.base/java.lang.Thread.run(Thread.java:1623) ~[na:na]

```

果然是其他的接口实现方法应i想了我们的程序

java.lang.NullPointerException: Cannot invoke "java.util.Map.get(Object)" because "map" is null at com.tulingxueyuan.mall.modules.oms.service.impl.OmsCartItemServiceImpl.getCarProdutSum(OmsCartItemServiceImpl.java:113)

1. 我们首先找到OmsCartltemServiceImpl.java

   ```java
   package com.tulingxueyuan.mall.modules.oms.service.impl;
   import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
   import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
   import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
   import com.tulingxueyuan.mall.common.api.ResultCode;
   import com.tulingxueyuan.mall.common.exception.Asserts;
   import com.tulingxueyuan.mall.dto.AddCarDTO;
   import com.tulingxueyuan.mall.modules.ums.service.UmsMemberService;
   import com.tulingxueyuan.mall.dto.CartItemStockDTO;
   import com.tulingxueyuan.mall.modules.oms.mapper.OmsCartItemMapper;
   import com.tulingxueyuan.mall.modules.oms.model.OmsCartItem;
   import com.tulingxueyuan.mall.modules.oms.service.OmsCartItemService;
   import com.tulingxueyuan.mall.modules.pms.model.PmsProduct;
   import com.tulingxueyuan.mall.modules.pms.model.PmsSkuStock;
   import com.tulingxueyuan.mall.modules.pms.service.PmsProductService;
   import com.tulingxueyuan.mall.modules.pms.service.PmsSkuStockService;
   import com.tulingxueyuan.mall.modules.ums.model.UmsMember;
   import org.springframework.beans.BeanUtils;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.stereotype.Service;
   import java.util.Date;
   import java.util.List;
   import java.util.Map;
   
   /**
    * <p>
    * 购物车表 服务实现类
    * </p>
    *
    * @author XuShu
    * @since 2021-03-19
    */
   @Service
   public class OmsCartItemServiceImpl extends ServiceImpl<OmsCartItemMapper, OmsCartItem> implements OmsCartItemService {
       @Autowired
       UmsMemberService memberService;
       @Autowired
       PmsSkuStockService skuStockService;
       @Autowired
       PmsProductService productService;
       @Autowired
       OmsCartItemMapper cartItemMapper;
       @Override
       public Boolean add(AddCarDTO addCarDTO) {
           OmsCartItem omsCartItem = new OmsCartItem();
           BeanUtils.copyProperties(addCarDTO,omsCartItem);
           UmsMember currentMember = memberService.getCurrentMember();
           omsCartItem.setMemberId(currentMember.getId());
           // 判断同一个商品、sku、用户 下是否添加的重复的购物车
           OmsCartItem cartItem = getCartItem(omsCartItem.getProductId(), omsCartItem.getProductSkuId(), omsCartItem.getMemberId());
           // 新增
           if(cartItem==null) {
               omsCartItem.setMemberNickname(currentMember.getNickname());
               // 查询sku
               PmsSkuStock sku = skuStockService.getById(omsCartItem.getProductSkuId());
               if (sku == null) Asserts.fail(ResultCode.VALIDATE_FAILED);
               omsCartItem.setPrice(sku.getPrice());
               omsCartItem.setSp1(sku.getSp1());
               omsCartItem.setSp2(sku.getSp2());
               omsCartItem.setSp3(sku.getSp3());
               omsCartItem.setProductPic(sku.getPic());
               omsCartItem.setProductSkuCode(sku.getSkuCode());
               PmsProduct product = productService.getById(omsCartItem.getProductId());
               if (product == null) Asserts.fail(ResultCode.VALIDATE_FAILED);
               omsCartItem.setProductName(product.getName());
               omsCartItem.setProductBrand(product.getBrandName());
               omsCartItem.setProductSn(product.getProductSn());
               omsCartItem.setProductSubTitle(product.getSubTitle());
               omsCartItem.setProductCategoryId(product.getProductCategoryId());
               omsCartItem.setCreateDate(new Date());
               omsCartItem.setModifyDate(new Date());
               return baseMapper.insert(omsCartItem)>0;
           }
           // 修改  给商品数量+1
           else {
               cartItem.setQuantity(cartItem.getQuantity()+1);
               cartItem.setModifyDate(new Date());
               UpdateWrapper<OmsCartItem> updateWrapper = new UpdateWrapper<>();
               updateWrapper.lambda()
                       .set(OmsCartItem::getQuantity,cartItem.getQuantity())
                       .set(OmsCartItem::getModifyDate,cartItem.getModifyDate())
                       .eq(OmsCartItem::getId,cartItem.getId());
              return baseMapper.update(cartItem,updateWrapper)>0;
           }
       }
   
       /**
        * getCarProdutSum
        * @return
        */
       @Override
       public Integer getCarProdutSum() {
           QueryWrapper<OmsCartItem> queryWrapper = new QueryWrapper<>();
           Long memberId = memberService.getCurrentMember().getId();
           // 查询当前用户的购物车商品的数量  1个字段
           queryWrapper
                   .select("sum(quantity) as total")
                   .lambda().eq(OmsCartItem::getMemberId,memberId);
   
           List<Map<String, Object>> list = baseMapper.selectMaps(queryWrapper);
           if(list!=null && list.size()==1){
               Map<String, Object> map = list.get(0);
               if(map.get("total")!=null){
                   return Integer.parseInt(map.get("total").toString());
               }
           }
           return 0;
       }
   
       /**
        * 初始化购物车数据
        * @return
        */
       @Override
       public List<CartItemStockDTO> getList() {
            // 1 当前用户
   
           UmsMember currentMember = memberService.getCurrentMember();
   
   
           List<CartItemStockDTO> list=cartItemMapper.getCartItemStock(currentMember.getId());
           return list;
       }
   
       /**
        * 更新商品数量
        * @param id
        * @param quantity
        * @return
        */
       @Override
       public boolean updateQuantity(Long id, Integer quantity) {
   
           UpdateWrapper<OmsCartItem> updateWrapper = new UpdateWrapper<>();
           updateWrapper.lambda()
                   .set(OmsCartItem::getQuantity,quantity)
                   .eq(OmsCartItem::getId,id);
   
           return this.update(updateWrapper);
       }
       @Override
       public Boolean delete(Long ids) {
           return this.removeById(ids);
       }
       /**
        * 判断同一个商品、sku、用户 下是否添加的重复的购物车
        * @param productId
        * @param skuId
        * @param memberId
        * @return
        */
       public OmsCartItem getCartItem(Long productId,Long skuId, Long memberId){
           QueryWrapper<OmsCartItem> queryWrapper = new QueryWrapper<>();
           queryWrapper.lambda()
                   .eq(OmsCartItem::getProductId,productId)
                   .eq(OmsCartItem::getProductSkuId,skuId)
                   .eq(OmsCartItem::getMemberId,memberId);
   
          return baseMapper.selectOne(queryWrapper);
       }
   }
   看的出来是一个购物车的业务逻辑
   在它空指针对象传输的过程中多加上校验代码
       List<Map<String, Object>> list = baseMapper.selectMaps(queryWrapper);
   if (list != null && !list.isEmpty()) {
       Map<String, Object> map = list.get(0);
       if (map.get("total") != null) {
           return Integer.parseInt(map.get("total").toString());
       }
   }
   return 0;
   
   ```

状态码99999=>空指针=>购物车非空字段=>修改检查字段方式=>jwt的权限校验=>...一系列的业务逻辑代码都是息息相关的！最终的底层就是我们的数据库设计的字段，所以大家务必把自己的数据库字段了解的清清楚楚！

接着上个视频我们来学习下后端mysql数据库这些问题怎么解决？

大概率是数据库表的问题？我们只有写好了最底层的查询，才能从根本上解决问题

![image-20231001214529041](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20231001214529041.png)

开发学习2：

为什么只显示一张图片呢？

![image-20231001215054476](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20231001215054476.png)

我们初步判断是前端出了问题，总结下，我们开发时候往往涉及到多个工具的学习使用，请大家认真学习这些测试接口的工具，努力成为一名合格的程序员！









