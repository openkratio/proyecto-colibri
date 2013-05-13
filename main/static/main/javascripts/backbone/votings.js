//Models
window.Voting = Backbone.Tastypie.Model.extend({
	url:"http://localhost:8000/api/v1/voting/",
});

window.VotingCollection = Backbone.Tastypie.Collection.extend({
	model:Voting,
	url:"http://localhost:8000/api/v1/voting/",
});

//Views
window.VotingListView = Backbone.View.extend({ 
	tagName:'ul', 
	initialize:function () {
		this.model.bind("reset", this.render, this);
	},
	render:function (eventName) {
		_.each(this.model.models, function (voting) {
			$(this.el).append(new VotingListItemView({model:voting}).render().el);
		}, this);
		return this;
	}
});

window.VotingListItemView = Backbone.View.extend({ 
	tagName:"li", 
	template:_.template($('#tpl-voting-list-item').html()), 
	render:function (eventName) {
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
	}
});

window.VotingView = Backbone.View.extend({ 
	template:_.template($('#tpl-voting-details').html()),
	render:function (eventName) {
		console.log(this.model.toJSON());
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
	}
});

// Router
var AppRouter = Backbone.Router.extend({
	routes:{
		"":"list",
	    "voting/:id":"votingDetails"
	},
	list:function () {
		this.votingList = new VotingCollection();
		this.votingListView = new VotingListView({model:this.votingList});
		this.votingList.fetch({
			success: function () {
				console.log("get ok");
				console.log(arguments);
			},
			error: function(){
				console.log("get fail");
				console.log(arguments);
			}
		});
		$('#sidebar').html(this.votingListView.render().el);
	}, 
	votingDetails:function (id) {
		this.voting = this.votingList.models[id];
		console.log(this.voting);
		this.votingView = new VotingView({model:this.voting});
		$('#content').html(this.votingView.render().el);
	}
});
 
var app = new AppRouter();
Backbone.history.start();
