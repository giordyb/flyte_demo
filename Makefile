all: create_project docker_build register_workflow

docker_build:
	IMAGE_NAME=flyte_test_image scripts/docker_build.sh

register_workflow:
	IMAGE_NAME=flyte_test_image scripts/register_workflow.sh

create_project:
	scripts/make_project.sh