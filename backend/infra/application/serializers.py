from rest_framework import serializers
from .models import ServiceRegistry, DependencyMap, DeploymentEvent, ConfigWatcher, KubernetesPod, KubernetesDeployment

class ServiceRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRegistry
        fields = '__all__'

class DependencyMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DependencyMap
        fields = '__all__'

class DeploymentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentEvent
        fields = '__all__'

class ConfigWatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigWatcher
        fields = '__all__'

class KubernetesPodSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesPod
        fields = '__all__'

class KubernetesDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesDeployment
        fields = '__all__'
