/**
 * Dashboard Statistics Component with Backend Integration
 */

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, CheckCircle, XCircle, AlertTriangle, Loader2 } from 'lucide-react';
import { useDashboardStats } from '@/hooks/use-api';

export function DashboardStats() {
  const { stats, loading, error } = useDashboardStats();

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <Card className="border-red-200 bg-red-50">
        <CardContent className="pt-6">
          <p className="text-red-900">Failed to load dashboard stats: {error}</p>
        </CardContent>
      </Card>
    );
  }

  if (!stats) {
    return null;
  }

  const statCards = [
    {
      title: 'Total Documents',
      value: stats.total_documents,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Average Confidence',
      value: `${stats.average_confidence.toFixed(1)}%`,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Compliance Rate',
      value: `${stats.compliance.pass_rate.toFixed(1)}%`,
      icon: stats.compliance.pass_rate >= 80 ? CheckCircle : AlertTriangle,
      color: stats.compliance.pass_rate >= 80 ? 'text-green-600' : 'text-orange-600',
      bgColor: stats.compliance.pass_rate >= 80 ? 'bg-green-100' : 'bg-orange-100',
    },
    {
      title: 'Total Errors',
      value: stats.total_errors,
      icon: XCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Main Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Detailed Stats */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Document Status Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle>Document Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {Object.entries(stats.status_breakdown).map(([status, count]) => (
                <div key={status} className="flex justify-between items-center">
                  <span className="text-sm capitalize">{status}</span>
                  <span className="font-medium">{count}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Compliance Details */}
        <Card>
          <CardHeader>
            <CardTitle>Compliance Checks</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm">Total Checks</span>
                <span className="font-medium">{stats.compliance.total_checks}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-green-600">Passed</span>
                <span className="font-medium text-green-600">
                  {stats.compliance.passed}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-red-600">Failed</span>
                <span className="font-medium text-red-600">
                  {stats.compliance.failed}
                </span>
              </div>
              <div className="pt-2 border-t">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Pass Rate</span>
                  <span className="font-bold">{stats.compliance.pass_rate.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity (Last 7 Days)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{stats.recent_activity}</div>
          <p className="text-sm text-gray-500 mt-1">documents processed</p>
        </CardContent>
      </Card>
    </div>
  );
}
