# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_rocketmq20220801 import models as rocket_mq20220801_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('rocketmq', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def change_resource_group_with_options(
        self,
        request: rocket_mq20220801_models.ChangeResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ChangeResourceGroupResponse:
        """
        @summary Changes the resource group to which a ApsaraMQ for RocketMQ instance belongs.
        
        @param request: ChangeResourceGroupRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ChangeResourceGroupResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['regionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['resourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_id):
            query['resourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            query['resourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ChangeResourceGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/resourceGroup/change',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ChangeResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def change_resource_group_with_options_async(
        self,
        request: rocket_mq20220801_models.ChangeResourceGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ChangeResourceGroupResponse:
        """
        @summary Changes the resource group to which a ApsaraMQ for RocketMQ instance belongs.
        
        @param request: ChangeResourceGroupRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ChangeResourceGroupResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['regionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['resourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_id):
            query['resourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            query['resourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ChangeResourceGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/resourceGroup/change',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ChangeResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def change_resource_group(
        self,
        request: rocket_mq20220801_models.ChangeResourceGroupRequest,
    ) -> rocket_mq20220801_models.ChangeResourceGroupResponse:
        """
        @summary Changes the resource group to which a ApsaraMQ for RocketMQ instance belongs.
        
        @param request: ChangeResourceGroupRequest
        @return: ChangeResourceGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.change_resource_group_with_options(request, headers, runtime)

    async def change_resource_group_async(
        self,
        request: rocket_mq20220801_models.ChangeResourceGroupRequest,
    ) -> rocket_mq20220801_models.ChangeResourceGroupResponse:
        """
        @summary Changes the resource group to which a ApsaraMQ for RocketMQ instance belongs.
        
        @param request: ChangeResourceGroupRequest
        @return: ChangeResourceGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.change_resource_group_with_options_async(request, headers, runtime)

    def create_consumer_group_with_options(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.CreateConsumerGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.CreateConsumerGroupResponse:
        """
        @summary Creates a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateConsumerGroupRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateConsumerGroupResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.consume_retry_policy):
            body['consumeRetryPolicy'] = request.consume_retry_policy
        if not UtilClient.is_unset(request.delivery_order_type):
            body['deliveryOrderType'] = request.delivery_order_type
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.CreateConsumerGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_consumer_group_with_options_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.CreateConsumerGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.CreateConsumerGroupResponse:
        """
        @summary Creates a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateConsumerGroupRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateConsumerGroupResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.consume_retry_policy):
            body['consumeRetryPolicy'] = request.consume_retry_policy
        if not UtilClient.is_unset(request.delivery_order_type):
            body['deliveryOrderType'] = request.delivery_order_type
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.CreateConsumerGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_consumer_group(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.CreateConsumerGroupRequest,
    ) -> rocket_mq20220801_models.CreateConsumerGroupResponse:
        """
        @summary Creates a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateConsumerGroupRequest
        @return: CreateConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_consumer_group_with_options(instance_id, consumer_group_id, request, headers, runtime)

    async def create_consumer_group_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.CreateConsumerGroupRequest,
    ) -> rocket_mq20220801_models.CreateConsumerGroupResponse:
        """
        @summary Creates a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateConsumerGroupRequest
        @return: CreateConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_consumer_group_with_options_async(instance_id, consumer_group_id, request, headers, runtime)

    def create_instance_with_options(
        self,
        request: rocket_mq20220801_models.CreateInstanceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.CreateInstanceResponse:
        """
        @summary Creates an ApsaraMQ for RocketMQ 5.x instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateInstanceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.client_token):
            query['clientToken'] = request.client_token
        body = {}
        if not UtilClient.is_unset(request.auto_renew):
            body['autoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.auto_renew_period):
            body['autoRenewPeriod'] = request.auto_renew_period
        if not UtilClient.is_unset(request.commodity_code):
            body['commodityCode'] = request.commodity_code
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.network_info):
            body['networkInfo'] = request.network_info
        if not UtilClient.is_unset(request.payment_type):
            body['paymentType'] = request.payment_type
        if not UtilClient.is_unset(request.period):
            body['period'] = request.period
        if not UtilClient.is_unset(request.period_unit):
            body['periodUnit'] = request.period_unit
        if not UtilClient.is_unset(request.product_info):
            body['productInfo'] = request.product_info
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.resource_group_id):
            body['resourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.series_code):
            body['seriesCode'] = request.series_code
        if not UtilClient.is_unset(request.service_code):
            body['serviceCode'] = request.service_code
        if not UtilClient.is_unset(request.sub_series_code):
            body['subSeriesCode'] = request.sub_series_code
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.CreateInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_instance_with_options_async(
        self,
        request: rocket_mq20220801_models.CreateInstanceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.CreateInstanceResponse:
        """
        @summary Creates an ApsaraMQ for RocketMQ 5.x instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateInstanceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.client_token):
            query['clientToken'] = request.client_token
        body = {}
        if not UtilClient.is_unset(request.auto_renew):
            body['autoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.auto_renew_period):
            body['autoRenewPeriod'] = request.auto_renew_period
        if not UtilClient.is_unset(request.commodity_code):
            body['commodityCode'] = request.commodity_code
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.network_info):
            body['networkInfo'] = request.network_info
        if not UtilClient.is_unset(request.payment_type):
            body['paymentType'] = request.payment_type
        if not UtilClient.is_unset(request.period):
            body['period'] = request.period
        if not UtilClient.is_unset(request.period_unit):
            body['periodUnit'] = request.period_unit
        if not UtilClient.is_unset(request.product_info):
            body['productInfo'] = request.product_info
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.resource_group_id):
            body['resourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.series_code):
            body['seriesCode'] = request.series_code
        if not UtilClient.is_unset(request.service_code):
            body['serviceCode'] = request.service_code
        if not UtilClient.is_unset(request.sub_series_code):
            body['subSeriesCode'] = request.sub_series_code
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.CreateInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_instance(
        self,
        request: rocket_mq20220801_models.CreateInstanceRequest,
    ) -> rocket_mq20220801_models.CreateInstanceResponse:
        """
        @summary Creates an ApsaraMQ for RocketMQ 5.x instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateInstanceRequest
        @return: CreateInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_instance_with_options(request, headers, runtime)

    async def create_instance_async(
        self,
        request: rocket_mq20220801_models.CreateInstanceRequest,
    ) -> rocket_mq20220801_models.CreateInstanceResponse:
        """
        @summary Creates an ApsaraMQ for RocketMQ 5.x instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: CreateInstanceRequest
        @return: CreateInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_instance_with_options_async(request, headers, runtime)

    def create_topic_with_options(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.CreateTopicRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.CreateTopicResponse:
        """
        @summary Creates a topic.
        
        @param request: CreateTopicRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateTopicResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.message_type):
            body['messageType'] = request.message_type
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.CreateTopicResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_topic_with_options_async(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.CreateTopicRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.CreateTopicResponse:
        """
        @summary Creates a topic.
        
        @param request: CreateTopicRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateTopicResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.message_type):
            body['messageType'] = request.message_type
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.CreateTopicResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_topic(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.CreateTopicRequest,
    ) -> rocket_mq20220801_models.CreateTopicResponse:
        """
        @summary Creates a topic.
        
        @param request: CreateTopicRequest
        @return: CreateTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.create_topic_with_options(instance_id, topic_name, request, headers, runtime)

    async def create_topic_async(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.CreateTopicRequest,
    ) -> rocket_mq20220801_models.CreateTopicResponse:
        """
        @summary Creates a topic.
        
        @param request: CreateTopicRequest
        @return: CreateTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.create_topic_with_options_async(instance_id, topic_name, request, headers, runtime)

    def delete_consumer_group_with_options(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.DeleteConsumerGroupResponse:
        """
        @summary Deletes a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After you delete a consumer group, the consumer client associated with the consumer group cannot consume messages. Exercise caution when you call this operation.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteConsumerGroupResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.DeleteConsumerGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_consumer_group_with_options_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.DeleteConsumerGroupResponse:
        """
        @summary Deletes a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After you delete a consumer group, the consumer client associated with the consumer group cannot consume messages. Exercise caution when you call this operation.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteConsumerGroupResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.DeleteConsumerGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_consumer_group(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.DeleteConsumerGroupResponse:
        """
        @summary Deletes a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After you delete a consumer group, the consumer client associated with the consumer group cannot consume messages. Exercise caution when you call this operation.
        
        @return: DeleteConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_consumer_group_with_options(instance_id, consumer_group_id, headers, runtime)

    async def delete_consumer_group_async(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.DeleteConsumerGroupResponse:
        """
        @summary Deletes a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After you delete a consumer group, the consumer client associated with the consumer group cannot consume messages. Exercise caution when you call this operation.
        
        @return: DeleteConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_consumer_group_with_options_async(instance_id, consumer_group_id, headers, runtime)

    def delete_instance_with_options(
        self,
        instance_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.DeleteInstanceResponse:
        """
        @summary Deletes a ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After an instance is deleted, the instance cannot be restored. Exercise caution when you call this operation.
        This operation is used to delete a pay-as-you-go instance. A subscription instance is automatically released after it expires. You do not need to manually delete a subscription instance.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteInstanceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.DeleteInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_instance_with_options_async(
        self,
        instance_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.DeleteInstanceResponse:
        """
        @summary Deletes a ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After an instance is deleted, the instance cannot be restored. Exercise caution when you call this operation.
        This operation is used to delete a pay-as-you-go instance. A subscription instance is automatically released after it expires. You do not need to manually delete a subscription instance.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteInstanceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.DeleteInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_instance(
        self,
        instance_id: str,
    ) -> rocket_mq20220801_models.DeleteInstanceResponse:
        """
        @summary Deletes a ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After an instance is deleted, the instance cannot be restored. Exercise caution when you call this operation.
        This operation is used to delete a pay-as-you-go instance. A subscription instance is automatically released after it expires. You do not need to manually delete a subscription instance.
        
        @return: DeleteInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_instance_with_options(instance_id, headers, runtime)

    async def delete_instance_async(
        self,
        instance_id: str,
    ) -> rocket_mq20220801_models.DeleteInstanceResponse:
        """
        @summary Deletes a ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        After an instance is deleted, the instance cannot be restored. Exercise caution when you call this operation.
        This operation is used to delete a pay-as-you-go instance. A subscription instance is automatically released after it expires. You do not need to manually delete a subscription instance.
        
        @return: DeleteInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_instance_with_options_async(instance_id, headers, runtime)

    def delete_topic_with_options(
        self,
        instance_id: str,
        topic_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.DeleteTopicResponse:
        """
        @summary Deletes a specified topic.
        
        @description If you delete the topic, the publishing and subscription relationships that are established based on the topic are cleared. Exercise caution when you call this operation.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteTopicResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.DeleteTopicResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_topic_with_options_async(
        self,
        instance_id: str,
        topic_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.DeleteTopicResponse:
        """
        @summary Deletes a specified topic.
        
        @description If you delete the topic, the publishing and subscription relationships that are established based on the topic are cleared. Exercise caution when you call this operation.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteTopicResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='DeleteTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.DeleteTopicResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_topic(
        self,
        instance_id: str,
        topic_name: str,
    ) -> rocket_mq20220801_models.DeleteTopicResponse:
        """
        @summary Deletes a specified topic.
        
        @description If you delete the topic, the publishing and subscription relationships that are established based on the topic are cleared. Exercise caution when you call this operation.
        
        @return: DeleteTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.delete_topic_with_options(instance_id, topic_name, headers, runtime)

    async def delete_topic_async(
        self,
        instance_id: str,
        topic_name: str,
    ) -> rocket_mq20220801_models.DeleteTopicResponse:
        """
        @summary Deletes a specified topic.
        
        @description If you delete the topic, the publishing and subscription relationships that are established based on the topic are cleared. Exercise caution when you call this operation.
        
        @return: DeleteTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.delete_topic_with_options_async(instance_id, topic_name, headers, runtime)

    def get_consumer_group_with_options(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.GetConsumerGroupResponse:
        """
        @summary Queries the details of a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetConsumerGroupResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.GetConsumerGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_consumer_group_with_options_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.GetConsumerGroupResponse:
        """
        @summary Queries the details of a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetConsumerGroupResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.GetConsumerGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_consumer_group(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.GetConsumerGroupResponse:
        """
        @summary Queries the details of a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @return: GetConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_consumer_group_with_options(instance_id, consumer_group_id, headers, runtime)

    async def get_consumer_group_async(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.GetConsumerGroupResponse:
        """
        @summary Queries the details of a specified consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @return: GetConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_consumer_group_with_options_async(instance_id, consumer_group_id, headers, runtime)

    def get_instance_with_options(
        self,
        instance_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.GetInstanceResponse:
        """
        @summary Queries the detailed information about an instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetInstanceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.GetInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_instance_with_options_async(
        self,
        instance_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.GetInstanceResponse:
        """
        @summary Queries the detailed information about an instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetInstanceResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.GetInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_instance(
        self,
        instance_id: str,
    ) -> rocket_mq20220801_models.GetInstanceResponse:
        """
        @summary Queries the detailed information about an instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @return: GetInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_instance_with_options(instance_id, headers, runtime)

    async def get_instance_async(
        self,
        instance_id: str,
    ) -> rocket_mq20220801_models.GetInstanceResponse:
        """
        @summary Queries the detailed information about an instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @return: GetInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_instance_with_options_async(instance_id, headers, runtime)

    def get_topic_with_options(
        self,
        instance_id: str,
        topic_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.GetTopicResponse:
        """
        @summary Queries the details of a specified topic.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetTopicResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.GetTopicResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_topic_with_options_async(
        self,
        instance_id: str,
        topic_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.GetTopicResponse:
        """
        @summary Queries the details of a specified topic.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetTopicResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='GetTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.GetTopicResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_topic(
        self,
        instance_id: str,
        topic_name: str,
    ) -> rocket_mq20220801_models.GetTopicResponse:
        """
        @summary Queries the details of a specified topic.
        
        @return: GetTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.get_topic_with_options(instance_id, topic_name, headers, runtime)

    async def get_topic_async(
        self,
        instance_id: str,
        topic_name: str,
    ) -> rocket_mq20220801_models.GetTopicResponse:
        """
        @summary Queries the details of a specified topic.
        
        @return: GetTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.get_topic_with_options_async(instance_id, topic_name, headers, runtime)

    def list_available_zones_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListAvailableZonesResponse:
        """
        @summary 查询支持的可用区
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListAvailableZonesResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListAvailableZones',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/zones',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListAvailableZonesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_available_zones_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListAvailableZonesResponse:
        """
        @summary 查询支持的可用区
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListAvailableZonesResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListAvailableZones',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/zones',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListAvailableZonesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_available_zones(self) -> rocket_mq20220801_models.ListAvailableZonesResponse:
        """
        @summary 查询支持的可用区
        
        @return: ListAvailableZonesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_available_zones_with_options(headers, runtime)

    async def list_available_zones_async(self) -> rocket_mq20220801_models.ListAvailableZonesResponse:
        """
        @summary 查询支持的可用区
        
        @return: ListAvailableZonesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_available_zones_with_options_async(headers, runtime)

    def list_consumer_connections_with_options(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListConsumerConnectionsResponse:
        """
        @summary 查询消费者客户端连接信息
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConsumerConnectionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListConsumerConnections',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}/connections',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListConsumerConnectionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_consumer_connections_with_options_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListConsumerConnectionsResponse:
        """
        @summary 查询消费者客户端连接信息
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConsumerConnectionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListConsumerConnections',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}/connections',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListConsumerConnectionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_consumer_connections(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.ListConsumerConnectionsResponse:
        """
        @summary 查询消费者客户端连接信息
        
        @return: ListConsumerConnectionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_consumer_connections_with_options(instance_id, consumer_group_id, headers, runtime)

    async def list_consumer_connections_async(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.ListConsumerConnectionsResponse:
        """
        @summary 查询消费者客户端连接信息
        
        @return: ListConsumerConnectionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_consumer_connections_with_options_async(instance_id, consumer_group_id, headers, runtime)

    def list_consumer_group_subscriptions_with_options(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListConsumerGroupSubscriptionsResponse:
        """
        @summary Queries the subscriptions of a consumer group.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConsumerGroupSubscriptionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListConsumerGroupSubscriptions',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}/subscriptions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListConsumerGroupSubscriptionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_consumer_group_subscriptions_with_options_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListConsumerGroupSubscriptionsResponse:
        """
        @summary Queries the subscriptions of a consumer group.
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConsumerGroupSubscriptionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListConsumerGroupSubscriptions',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}/subscriptions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListConsumerGroupSubscriptionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_consumer_group_subscriptions(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.ListConsumerGroupSubscriptionsResponse:
        """
        @summary Queries the subscriptions of a consumer group.
        
        @return: ListConsumerGroupSubscriptionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_consumer_group_subscriptions_with_options(instance_id, consumer_group_id, headers, runtime)

    async def list_consumer_group_subscriptions_async(
        self,
        instance_id: str,
        consumer_group_id: str,
    ) -> rocket_mq20220801_models.ListConsumerGroupSubscriptionsResponse:
        """
        @summary Queries the subscriptions of a consumer group.
        
        @return: ListConsumerGroupSubscriptionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_consumer_group_subscriptions_with_options_async(instance_id, consumer_group_id, headers, runtime)

    def list_consumer_groups_with_options(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.ListConsumerGroupsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListConsumerGroupsResponse:
        """
        @summary Queries the consumer groups in a specified instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: ListConsumerGroupsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConsumerGroupsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.filter):
            query['filter'] = request.filter
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListConsumerGroups',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListConsumerGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_consumer_groups_with_options_async(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.ListConsumerGroupsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListConsumerGroupsResponse:
        """
        @summary Queries the consumer groups in a specified instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: ListConsumerGroupsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListConsumerGroupsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.filter):
            query['filter'] = request.filter
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListConsumerGroups',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListConsumerGroupsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_consumer_groups(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.ListConsumerGroupsRequest,
    ) -> rocket_mq20220801_models.ListConsumerGroupsResponse:
        """
        @summary Queries the consumer groups in a specified instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: ListConsumerGroupsRequest
        @return: ListConsumerGroupsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_consumer_groups_with_options(instance_id, request, headers, runtime)

    async def list_consumer_groups_async(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.ListConsumerGroupsRequest,
    ) -> rocket_mq20220801_models.ListConsumerGroupsResponse:
        """
        @summary Queries the consumer groups in a specified instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: ListConsumerGroupsRequest
        @return: ListConsumerGroupsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_consumer_groups_with_options_async(instance_id, request, headers, runtime)

    def list_instances_with_options(
        self,
        tmp_req: rocket_mq20220801_models.ListInstancesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListInstancesResponse:
        """
        @summary Queries instances.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param tmp_req: ListInstancesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListInstancesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = rocket_mq20220801_models.ListInstancesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.series_codes):
            request.series_codes_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.series_codes, 'seriesCodes', 'simple')
        query = {}
        if not UtilClient.is_unset(request.filter):
            query['filter'] = request.filter
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_group_id):
            query['resourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.series_codes_shrink):
            query['seriesCodes'] = request.series_codes_shrink
        if not UtilClient.is_unset(request.tags):
            query['tags'] = request.tags
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstances',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListInstancesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_instances_with_options_async(
        self,
        tmp_req: rocket_mq20220801_models.ListInstancesRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListInstancesResponse:
        """
        @summary Queries instances.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param tmp_req: ListInstancesRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListInstancesResponse
        """
        UtilClient.validate_model(tmp_req)
        request = rocket_mq20220801_models.ListInstancesShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.series_codes):
            request.series_codes_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.series_codes, 'seriesCodes', 'simple')
        query = {}
        if not UtilClient.is_unset(request.filter):
            query['filter'] = request.filter
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_group_id):
            query['resourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.series_codes_shrink):
            query['seriesCodes'] = request.series_codes_shrink
        if not UtilClient.is_unset(request.tags):
            query['tags'] = request.tags
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListInstances',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListInstancesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_instances(
        self,
        request: rocket_mq20220801_models.ListInstancesRequest,
    ) -> rocket_mq20220801_models.ListInstancesResponse:
        """
        @summary Queries instances.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: ListInstancesRequest
        @return: ListInstancesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_instances_with_options(request, headers, runtime)

    async def list_instances_async(
        self,
        request: rocket_mq20220801_models.ListInstancesRequest,
    ) -> rocket_mq20220801_models.ListInstancesResponse:
        """
        @summary Queries instances.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: ListInstancesRequest
        @return: ListInstancesResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_instances_with_options_async(request, headers, runtime)

    def list_regions_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListRegionsResponse:
        """
        @summary 查询region列表
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRegionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListRegions',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/regions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListRegionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_regions_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListRegionsResponse:
        """
        @summary 查询region列表
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListRegionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListRegions',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/regions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListRegionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_regions(self) -> rocket_mq20220801_models.ListRegionsResponse:
        """
        @summary 查询region列表
        
        @return: ListRegionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_regions_with_options(headers, runtime)

    async def list_regions_async(self) -> rocket_mq20220801_models.ListRegionsResponse:
        """
        @summary 查询region列表
        
        @return: ListRegionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_regions_with_options_async(headers, runtime)

    def list_topic_subscriptions_with_options(
        self,
        instance_id: str,
        topic_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListTopicSubscriptionsResponse:
        """
        @summary 查询主题订阅关系列表
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTopicSubscriptionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListTopicSubscriptions',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}/subscriptions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListTopicSubscriptionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_topic_subscriptions_with_options_async(
        self,
        instance_id: str,
        topic_name: str,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListTopicSubscriptionsResponse:
        """
        @summary 查询主题订阅关系列表
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTopicSubscriptionsResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='ListTopicSubscriptions',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}/subscriptions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListTopicSubscriptionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_topic_subscriptions(
        self,
        instance_id: str,
        topic_name: str,
    ) -> rocket_mq20220801_models.ListTopicSubscriptionsResponse:
        """
        @summary 查询主题订阅关系列表
        
        @return: ListTopicSubscriptionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_topic_subscriptions_with_options(instance_id, topic_name, headers, runtime)

    async def list_topic_subscriptions_async(
        self,
        instance_id: str,
        topic_name: str,
    ) -> rocket_mq20220801_models.ListTopicSubscriptionsResponse:
        """
        @summary 查询主题订阅关系列表
        
        @return: ListTopicSubscriptionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_topic_subscriptions_with_options_async(instance_id, topic_name, headers, runtime)

    def list_topics_with_options(
        self,
        instance_id: str,
        tmp_req: rocket_mq20220801_models.ListTopicsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListTopicsResponse:
        """
        @summary Queries the topics in a specified instance.
        
        @param tmp_req: ListTopicsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTopicsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = rocket_mq20220801_models.ListTopicsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.message_types):
            request.message_types_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.message_types, 'messageTypes', 'simple')
        query = {}
        if not UtilClient.is_unset(request.filter):
            query['filter'] = request.filter
        if not UtilClient.is_unset(request.message_types_shrink):
            query['messageTypes'] = request.message_types_shrink
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTopics',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListTopicsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_topics_with_options_async(
        self,
        instance_id: str,
        tmp_req: rocket_mq20220801_models.ListTopicsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ListTopicsResponse:
        """
        @summary Queries the topics in a specified instance.
        
        @param tmp_req: ListTopicsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTopicsResponse
        """
        UtilClient.validate_model(tmp_req)
        request = rocket_mq20220801_models.ListTopicsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.message_types):
            request.message_types_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.message_types, 'messageTypes', 'simple')
        query = {}
        if not UtilClient.is_unset(request.filter):
            query['filter'] = request.filter
        if not UtilClient.is_unset(request.message_types_shrink):
            query['messageTypes'] = request.message_types_shrink
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTopics',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ListTopicsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_topics(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.ListTopicsRequest,
    ) -> rocket_mq20220801_models.ListTopicsResponse:
        """
        @summary Queries the topics in a specified instance.
        
        @param request: ListTopicsRequest
        @return: ListTopicsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.list_topics_with_options(instance_id, request, headers, runtime)

    async def list_topics_async(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.ListTopicsRequest,
    ) -> rocket_mq20220801_models.ListTopicsResponse:
        """
        @summary Queries the topics in a specified instance.
        
        @param request: ListTopicsRequest
        @return: ListTopicsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.list_topics_with_options_async(instance_id, request, headers, runtime)

    def reset_consume_offset_with_options(
        self,
        instance_id: str,
        consumer_group_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.ResetConsumeOffsetRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ResetConsumeOffsetResponse:
        """
        @summary Resets the consumer offset of a consumer group.
        
        @param request: ResetConsumeOffsetRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ResetConsumeOffsetResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.reset_time):
            body['resetTime'] = request.reset_time
        if not UtilClient.is_unset(request.reset_type):
            body['resetType'] = request.reset_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ResetConsumeOffset',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}/consumeOffsets/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ResetConsumeOffsetResponse(),
            self.call_api(params, req, runtime)
        )

    async def reset_consume_offset_with_options_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.ResetConsumeOffsetRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.ResetConsumeOffsetResponse:
        """
        @summary Resets the consumer offset of a consumer group.
        
        @param request: ResetConsumeOffsetRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ResetConsumeOffsetResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.reset_time):
            body['resetTime'] = request.reset_time
        if not UtilClient.is_unset(request.reset_type):
            body['resetType'] = request.reset_type
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ResetConsumeOffset',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}/consumeOffsets/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.ResetConsumeOffsetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def reset_consume_offset(
        self,
        instance_id: str,
        consumer_group_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.ResetConsumeOffsetRequest,
    ) -> rocket_mq20220801_models.ResetConsumeOffsetResponse:
        """
        @summary Resets the consumer offset of a consumer group.
        
        @param request: ResetConsumeOffsetRequest
        @return: ResetConsumeOffsetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.reset_consume_offset_with_options(instance_id, consumer_group_id, topic_name, request, headers, runtime)

    async def reset_consume_offset_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.ResetConsumeOffsetRequest,
    ) -> rocket_mq20220801_models.ResetConsumeOffsetResponse:
        """
        @summary Resets the consumer offset of a consumer group.
        
        @param request: ResetConsumeOffsetRequest
        @return: ResetConsumeOffsetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.reset_consume_offset_with_options_async(instance_id, consumer_group_id, topic_name, request, headers, runtime)

    def update_consumer_group_with_options(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.UpdateConsumerGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.UpdateConsumerGroupResponse:
        """
        @summary Updates the basic information about and the consumption retry policy of a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateConsumerGroupRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateConsumerGroupResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.consume_retry_policy):
            body['consumeRetryPolicy'] = request.consume_retry_policy
        if not UtilClient.is_unset(request.delivery_order_type):
            body['deliveryOrderType'] = request.delivery_order_type
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.UpdateConsumerGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_consumer_group_with_options_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.UpdateConsumerGroupRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.UpdateConsumerGroupResponse:
        """
        @summary Updates the basic information about and the consumption retry policy of a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateConsumerGroupRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateConsumerGroupResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.consume_retry_policy):
            body['consumeRetryPolicy'] = request.consume_retry_policy
        if not UtilClient.is_unset(request.delivery_order_type):
            body['deliveryOrderType'] = request.delivery_order_type
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateConsumerGroup',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/consumerGroups/{OpenApiUtilClient.get_encode_param(consumer_group_id)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.UpdateConsumerGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_consumer_group(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.UpdateConsumerGroupRequest,
    ) -> rocket_mq20220801_models.UpdateConsumerGroupResponse:
        """
        @summary Updates the basic information about and the consumption retry policy of a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateConsumerGroupRequest
        @return: UpdateConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_consumer_group_with_options(instance_id, consumer_group_id, request, headers, runtime)

    async def update_consumer_group_async(
        self,
        instance_id: str,
        consumer_group_id: str,
        request: rocket_mq20220801_models.UpdateConsumerGroupRequest,
    ) -> rocket_mq20220801_models.UpdateConsumerGroupResponse:
        """
        @summary Updates the basic information about and the consumption retry policy of a consumer group.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateConsumerGroupRequest
        @return: UpdateConsumerGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_consumer_group_with_options_async(instance_id, consumer_group_id, request, headers, runtime)

    def update_instance_with_options(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.UpdateInstanceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.UpdateInstanceResponse:
        """
        @summary Updates the basic information and specifications of an ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateInstanceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.acl_info):
            body['aclInfo'] = request.acl_info
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.network_info):
            body['networkInfo'] = request.network_info
        if not UtilClient.is_unset(request.product_info):
            body['productInfo'] = request.product_info
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.UpdateInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_instance_with_options_async(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.UpdateInstanceRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.UpdateInstanceResponse:
        """
        @summary Updates the basic information and specifications of an ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateInstanceRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.acl_info):
            body['aclInfo'] = request.acl_info
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.network_info):
            body['networkInfo'] = request.network_info
        if not UtilClient.is_unset(request.product_info):
            body['productInfo'] = request.product_info
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateInstance',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.UpdateInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_instance(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.UpdateInstanceRequest,
    ) -> rocket_mq20220801_models.UpdateInstanceResponse:
        """
        @summary Updates the basic information and specifications of an ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateInstanceRequest
        @return: UpdateInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_instance_with_options(instance_id, request, headers, runtime)

    async def update_instance_async(
        self,
        instance_id: str,
        request: rocket_mq20220801_models.UpdateInstanceRequest,
    ) -> rocket_mq20220801_models.UpdateInstanceResponse:
        """
        @summary Updates the basic information and specifications of an ApsaraMQ for RocketMQ instance.
        
        @description > API operations provided by Alibaba Cloud are used to manage and query resources of Alibaba Cloud services. We recommend that you integrate these API operations only in management systems. Do not use these API operations in the core system of messaging services. Otherwise, system risks may occur.
        
        @param request: UpdateInstanceRequest
        @return: UpdateInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_instance_with_options_async(instance_id, request, headers, runtime)

    def update_topic_with_options(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.UpdateTopicRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.UpdateTopicResponse:
        """
        @summary Updates the basic information about a topic.
        
        @param request: UpdateTopicRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateTopicResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.UpdateTopicResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_topic_with_options_async(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.UpdateTopicRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> rocket_mq20220801_models.UpdateTopicResponse:
        """
        @summary Updates the basic information about a topic.
        
        @param request: UpdateTopicRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpdateTopicResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateTopic',
            version='2022-08-01',
            protocol='HTTPS',
            pathname=f'/instances/{OpenApiUtilClient.get_encode_param(instance_id)}/topics/{OpenApiUtilClient.get_encode_param(topic_name)}',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            rocket_mq20220801_models.UpdateTopicResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_topic(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.UpdateTopicRequest,
    ) -> rocket_mq20220801_models.UpdateTopicResponse:
        """
        @summary Updates the basic information about a topic.
        
        @param request: UpdateTopicRequest
        @return: UpdateTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.update_topic_with_options(instance_id, topic_name, request, headers, runtime)

    async def update_topic_async(
        self,
        instance_id: str,
        topic_name: str,
        request: rocket_mq20220801_models.UpdateTopicRequest,
    ) -> rocket_mq20220801_models.UpdateTopicResponse:
        """
        @summary Updates the basic information about a topic.
        
        @param request: UpdateTopicRequest
        @return: UpdateTopicResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.update_topic_with_options_async(instance_id, topic_name, request, headers, runtime)
