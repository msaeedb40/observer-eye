from rest_framework import serializers
from .models import SystemResource, KubernetesCluster, KubernetesNode, KubernetesPod, CloudResource

class SystemResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemResource
        fields = '__all__'

class KubernetesClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesCluster
        fields = '__all__'

class KubernetesNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesNode
        fields = '__all__'

class KubernetesPodSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesPod
        fields = '__all__'

class CloudResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudResource
        fields = '__all__'
