var client = new Keen({
  projectId: '5368fa5436bf5a5623000000',
  readKey: '3f324dcb5636316d6865ab0ebbbbc725224c7f8f3e8899c7733439965d6d4a2c7f13bf7765458790bd50ec76b4361687f51cf626314585dc246bb51aeb455c0a1dd6ce77a993d9c953c5fc554d1d3530ca5d17bdc6d1333ef3d8146a990c79435bb2c7d936f259a22647a75407921056'
});

Keen.ready(function(){

  // Pageviews by browser

  var pageviews_timeline = new Keen.Dataviz()
    .el('#chart-01')
    .type('area')
    .height(280)
    .stacked(true)
    .title('Pageviews by browser')
    .prepare();

  client
    .query('count', {
      event_collection: 'pageviews',
      interval: 'hourly',
      group_by: 'user.device_info.browser.family',
      timeframe: {
        start: '2014-05-04T00:00:00.000Z',
        end: '2014-05-05T00:00:00.000Z'
      }
    })
    .then(function(res) {
      pageviews_timeline
        .data(res)
        .sortGroups('desc')
        .render();
    })
    .catch(function(err) {
      pageviews_timeline.message(err.message)
    });


  // Pageviews by browser (pie)

  var pageviews_pie = new Keen.Dataviz()
    .el('#chart-02')
    .type('pie')
    .height(280)
    .title('Pageviews by browser')
    .prepare();

  client
    .query('count', {
      event_collection: 'pageviews',
      group_by: 'user.device_info.browser.family',
      timeframe: {
        start: '2014-05-01T00:00:00.000Z',
        end: '2014-05-05T00:00:00.000Z'
      }
    })
    .then(function(res) {
      pageviews_pie
        .data(res)
        .sortGroups('desc')
        .render();
    })
    .catch(function(err) {
      pageviews_pie.message(err.message)
    });


  // Impressions timeline

  var impressions_timeline = new Keen.Dataviz()
    .el('#chart-03')
    .type('bar')
    .height(280)
    .stacked(true)
    .title('Impressions by advertiser')
    .prepare();

  client
    .query('count', {
      event_collection: 'impressions',
      group_by: 'ad.advertiser',
      interval: 'hourly',
      timeframe: {
        start: '2014-05-04T00:00:00.000Z',
        end: '2014-05-05T00:00:00.000Z'
      }
    })
    .then(function(res) {
      impressions_timeline
        .data(res)
        .sortGroups('desc')
        .render();
    })
    .catch(function(err) {
      impressions_timeline.message(err.message)
    });
});
