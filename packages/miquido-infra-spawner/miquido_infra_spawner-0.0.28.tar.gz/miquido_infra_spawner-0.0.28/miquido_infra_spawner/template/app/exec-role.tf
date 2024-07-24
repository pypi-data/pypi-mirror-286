resource "aws_iam_role" "execution-role" {
  name               = "${var.project}-${var.environment}-execution-role"
  description        = "Role used for executing tasks in ECS"
  assume_role_policy = data.aws_iam_policy_document.execution.json
}

data "aws_iam_policy_document" "execution" {
  version = "2012-10-17"

  statement {
    sid     = "AllowAssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["892651288265"]
    }

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["true"]
    }

    condition {
      test     = "Bool"
      variable = "aws:MultiFactorAuthPresent"
      values   = ["true"]
    }
  }
}

data "aws_iam_policy_document" "api-policy" {
  statement {
    actions = [
      "ecs:ExecuteCommand",
      "ecs:DescribeTasks"
    ]

    resources = [
      local.ecs_cluster_arn,
      "${replace(local.ecs_cluster_arn, "cluster", "task")}*"
    ]
  }

}

resource "aws_iam_role_policy" "api-policy" {
  policy = data.aws_iam_policy_document.api-policy.json
  role   = aws_iam_role.execution-role.name
}